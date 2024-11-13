import streamlit as sl
from streamlit_option_menu import option_menu
import duckdb as db

import base64
import glob
import os
import pathlib
from os.path import basename

from components.metric import total_monitored, total_monitored_rpt, plot, table,  get_reference, clean_data, plot_chart, get_prev_week
from components.gen_report import PDF

# ========= Page setup ======================
sl.set_page_config(page_title="Classroom Monitoring Dashboard", page_icon=":bar_chart:", layout="wide")

from components.css import css

# go to webfx.com/tools/emoji-cheat-sheet/ for emoji's

# ========= CSS ===============
sl.markdown(css, unsafe_allow_html=True)

sl.header("Classroom Monitoring Dashboard :bar_chart:")

# with sl.sidebar:
#     selected = option_menu(
#         menu_title="Dashboard",
#         options=["Trips", "Routes"],
#         icons=["bicycle", "compass"],
#         default_index=0,
#         orientation="vertical",
#     )
#     "---"

data = clean_data()

with sl.sidebar:
    sess = data["session"].unique()
    sem = data["semester"].unique()
    wee = data["week"].unique()
    session = sl.selectbox("Filter by Session", options=sess, index=len(sess)-1)
    semester = sl.selectbox("Filter by Semester", options=sem, index=len(sem)-1)
    week = sl.selectbox("Filter by Week", options=wee, index=len(wee)-1)

    filtered_df = data.query("session == @session and semester == @semester and week == @week")

left_col, center_col, right_col = sl.columns(3)
prev_week = get_prev_week(week, data)

with left_col:
    ref_total = get_reference(week, data)
    # print(ref_total)
    # get fig and display chart
    tot_monitored = total_monitored(filtered_df.shape[0], 'Total Classes Monitored', reference=ref_total)
    tot_monitored_rept = total_monitored_rpt(filtered_df.shape[0], 'Total Classes Monitored', reference=ref_total)

    tot_monitored_rept.write_image(
        'total_mon.png',
        engine="kaleido",
        format="png",
        scale=2,
    )

    sl.plotly_chart(tot_monitored, use_container_width=True)

with center_col:
    # Total classes that held
    held = filtered_df[(filtered_df['observation'] == 'The Teacher was Present In Class') | (filtered_df['observation'] == '--Select--')]
    ref_held = get_reference(week, data, held='held')
    total_held = total_monitored(held.shape[0], 'Total Classes Held', reference=ref_held)
    total_held_rpt = total_monitored_rpt(held.shape[0], 'Total Classes Held', reference=ref_held)

    total_held_rpt.write_image(
        'total_held.png',
        engine="kaleido",
        format="png",
        scale=2,
    )

    sl.plotly_chart(total_held, use_container_width=True)

with right_col:
    # Total classes that held
    not_held = filtered_df[(filtered_df['observation'] == 'The Class did not hold') | (filtered_df['observation'] == 'The Teacher was Absent From Class') | (filtered_df['observation'] == 'The Teacher was present but left early') | (filtered_df['observation'] == '--Select--')]
    ref_not_held = get_reference(week, data, held='not held')
    total_not_held = total_monitored(not_held.shape[0], 'Total Classes Not Held', reference=ref_not_held)
    total_not_held_rpt = total_monitored_rpt(not_held.shape[0], 'Total Classes Not Held', reference=ref_not_held)

    total_not_held_rpt.write_image(
        'total_not_held.png',
        engine="kaleido",
        format="png",
        scale=2,
    )

    sl.plotly_chart(total_not_held, use_container_width=True)

"---"
tot_school, tot_daily = sl.columns(2)

with tot_school:
    # Total monitored by school
    school = db.sql(
        f"""
            SELECT
                school,
                COUNT(school) as Monitored
            FROM filtered_df
            GROUP BY school
            ORDER BY Monitored
        """
    ).df()

    school_prev = db.sql(
        f"""
            SELECT
                school,
                COUNT(school) as Monitored
            FROM prev_week
            GROUP BY school
            ORDER BY Monitored
        """
    ).df()

    school_stats = school["Monitored"].describe().round(1)

    # print(f'monitored stats: {stats}')

    monitored_by_school = plot(school, x='Monitored', y='school', title=f'Total Class Monitored By School - Week {week}', line=False)

    school_reference = [school_stats['mean'], school_stats['std']]
    monitored_by_school_rpt = plot_chart(school, y='Monitored', x='school', title=f'Total Class Monitored By School - Week {week}', line=False, text=school['Monitored'], margin_left=45, prev_week=school_prev, week=week, reference=school_reference)

    monitored_by_school_rpt.write_image(
        'monitored_by_school.png',
        engine="kaleido",
        format="png",
        # scale=2,
    )

with tot_daily:
    # Total monitored daily
    daily = db.sql(
        f"""
            SELECT
                day,
                day_num,
                COUNT(coursecode) as Monitored
            FROM filtered_df
            WHERE day in ('Monday','Tuesday','Wednesday','Thursday','Friday')
            GROUP BY day, day_num
            ORDER BY day_num
        """
    ).df()

    daily_prev = db.sql(
        f"""
            SELECT
                day,
                day_num,
                COUNT(coursecode) as Monitored
            FROM prev_week
            WHERE day in ('Monday','Tuesday','Wednesday','Thursday','Friday')
            GROUP BY day, day_num
            ORDER BY day_num
        """
    ).df()

    monitored_by_day = plot(daily,'day','Monitored', title=f'Total Class Monitored By Day - Week {week}')
    monitored_by_day_rpt = plot_chart(daily, x='day', y='Monitored', title=f'Total Class Monitored By Day - Week {week}', margin_left=45, prev_week=daily_prev, week=week)

    monitored_by_day_rpt.write_image(
        'monitored_by_day.png',
        engine="kaleido",
        format="png",
        # scale=2,
    )

# The classes that did not hold
unheld_class_rpt_sec, unheld_class_rpt, unheld_class = table(filtered_df, title=f'List of Classes that did not hold - Week {week}')

sl.plotly_chart(unheld_class, use_container_width=True)

agent_tot, agent_daily = sl.columns(2)

with agent_tot:
    # Total monitored by officers
    # filtered_df.loc[:, 'Reporter'] = filtered_df['Reporter'].apply(recode)
    reporter = db.sql(
        f"""
            SELECT
                reporter,
                COUNT(school) as Monitored
            FROM filtered_df
            GROUP BY reporter
            ORDER BY Monitored
        """
    ).df()

    reporter_prev = db.sql(
        f"""
            SELECT
                reporter,
                COUNT(school) as Monitored
            FROM prev_week
            GROUP BY reporter
            ORDER BY Monitored
        """
    ).df()

    # reporter = reporter[reporter['Reporter'] != 'Unspecified']

    reporter_stats = reporter["Monitored"].describe().round(1)

    monitored_agent = plot(reporter, 'Monitored', 'reporter', title=f'Total Classes Monitored per Officer - Week {week}', line=False)

    reporter_reference = [reporter_stats['mean'], reporter_stats['std']]
    monitored_by_agent_rpt = plot_chart(reporter, y='Monitored', x='reporter', title=f'Total Class Monitored By Officers - Week {week}', line=False, text=reporter['Monitored'], margin_left=45, prev_week=reporter_prev, week=week, not_school=True, reference=reporter_reference)

    monitored_by_agent_rpt.write_image(
        'monitored_by_agent.png',
        engine="kaleido",
        format="png",
        # scale=2,
    )

with agent_daily:
    # Total monitored agent day
    daily_rp = db.sql(
        f"""
            SELECT
                day,
                day_num,
                reporter,
                COUNT(coursecode) as Monitored
            FROM filtered_df
            WHERE day in ('Monday','Tuesday','Wednesday','Thursday','Friday')
            GROUP BY day, day_num, Reporter
            ORDER BY day_num asc
        """
    ).df()

    # daily_rp = daily_rp[daily_rp['Reporter'] != 'Unspecified']

    monitored_agent_day = plot(daily_rp, 'day', 'Monitored', f'Total Classes Monitored per Officer by Day - Week {week}', color='reporter')

# "---"



# # sl.write(prev_week)

# reporter_prev = db.sql(
#     f"""
#         SELECT
#             reporter,
#             COUNT(school) as Monitored
#         FROM prev_week
#         GROUP BY reporter
#         ORDER BY Monitored
#     """
# ).df()

# monitored_by_officer = plot_chart(reporter, y='Monitored', x='reporter', title=f'Total Class Monitored By Officers - Week {week}', line=False, text=reporter['Monitored'], margin_left=5, prev_week=reporter_prev, week=week)

# sl.plotly_chart(monitored_by_day_rpt, use_container_width=False)

with sl.sidebar:
    "---"
    report_btn = sl.button("Generate Report")

    if report_btn:
        # save total monitored KPI as png

        pdf = PDF("L", "mm", "A4")
        pdf.add_page()

        # add header information
        pdf.set_header(week)

        unheld_class_rpt_sec = unheld_class_rpt_sec.sort_values(by="School")
        
        # display kpi cards
        pdf.display_kpi()

        # display total by school and by day
        pdf.display_by_school()

        # list classes that did not hold
        pdf.add_page()
        pdf.unheld(unheld_class_rpt_sec, "List of Classes that did not hold", sec=True)

        pdf.display_by_agent()

        # get pdf files in current directory
        pdf_file_path = glob.glob(os.path.join(os.getcwd(), "weekly monitoring report.pdf"))
        # sl.write(pdf_file_path)
        # make files available for download and remove from current directory
        for report_path in pdf_file_path:
            # extract the file name
            report_name = report_path.split("/")[-1]
            report_name = report_name.split(".")[0]

            # read pdf file and convert to base64 string
            with open(
                "{}.pdf".format(report_name),
                "rb",
            ) as pdf_file:
                pdf_base64 = base64.b64encode(pdf_file.read()).decode(
                    "utf-8"
                )

            sl.markdown(
                f"{pdf.report_download(pdf_base64, report_name)} :white",
                unsafe_allow_html=True,
            )

    # if report_btn:
    #     # save total monitored KPI as png

    #     pdf = PDF("L", "mm", "A4")
    #     pdf.add_page()

    #     # add header information
    #     pdf.set_header(week)

    #     unheld_class_rpt_sec = unheld_class_rpt_sec.sort_values(by="School")

    #     # list classes that did not hold
    #     pdf.unheld(unheld_class_rpt_sec, "List of Classes that did not hold", sec=True)

    #     # get pdf files in current directory
    #     pdf_file_path = glob.glob(os.path.join(os.getcwd(), "weekly monitoring report - sec.pdf"))

    #     # make files available for download and remove from current directory
    #     for report_path in pdf_file_path:
    #         # extract the file name
    #         report_name = report_path.split("/")[-1]
    #         report_name = report_name.split(".")[0]

    #         # read pdf file and convert to base64 string
    #         with open(
    #             "{}.pdf".format(report_name),
    #             "rb",
    #         ) as pdf_file:
    #             pdf_base64 = base64.b64encode(pdf_file.read()).decode(
    #                 "utf-8"
    #             )

    #         sl.markdown(
    #             f"{pdf.report_download(pdf_base64, report_name, sec=True)} :white",
    #             unsafe_allow_html=True,
    #         )

            # if os.path.exists("{}.pdf".format(report_name)):
            #     os.remove("{}.pdf".format(report_name))