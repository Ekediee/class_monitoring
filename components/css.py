import streamlit as sl

css = f"""
    <style>
        section[data-testid='stSidebar']{{
            width: 200px !important;
            # background: #FFF;
        }}
        div[class='block-container css-z5fcl4 e1g8pov64']{{
            padding-right: 1.5rem;
            padding-left: 1.5rem;
        }}
        hr{{
            margin-top: 1em;
            margin-bottom: 1em;
        }}
        div[data-testid='stToolbar']{{
            display: none !important;
        }}
        a[class='modebar-btn plotlyjsicon modebar-btn--logo']{{
            display: none !important;
        }}
        footer{{
            display: none !important;
        }}
        div[data-testid='block-container']{{
            padding-top: 0rem;
        }}
        # div[data-testid='stVerticalBlock']{{
        #     gap: 0rem;
        # }}
        # div[class='css-12w0qpk esravye1']{{
        #     background: #444444;
        #     # border: 5px solid #FFF;
        #     padding: 5px;
        #     border-radius: 1rem;
        #     # border-left: 0.1rem solid #9AD8E1 !important;
        #     box-shadow: 0.1rem 0.1rem 0.2rem 0 #a8a9a9 !important;
        # }}
        # div[class='css-1r6slb0 esravye1']{{
        #     background: #444444;
        #     # border: 5px solid #FFF;
        #     padding: 5px;
        #     border-radius: 1rem;
        #     # border-left: 0.1rem solid #9AD8E1 !important;
        #     box-shadow: 0.1rem 0.1rem 0.2rem 0 #a8a9a9 !important;
        # }}
        div[class='stPlotlyChart js-plotly-plot']{{
            background: white;
            outline: 40px solid white
            # border: 5px solid #FFF;
            # margin-right: 4px;
            padding: 3px;
            border-radius: 10px;
            # border-left: 0.1rem solid #9AD8E1 !important;
            box-shadow: 0.1rem 0.1rem 0.2rem 0 rgba(135,135,135,0.7) !important;
            display: flex;
            justify-content: center;
        }}
        # g[class='legend']{{
        #     display: none !important;
        # }}
        header{{
            display: none !important;
        }}
        @media only screen and (max-width: 550px) {{
            g[clip-path='url(#legendc8a499)']{{
                display: none !important;
            }}
        }}
    </style>
"""
