import inspect
import textwrap
from collections import OrderedDict

import registration
import recognize_faces
import show_database


import streamlit as st
from streamlit.hello import demos
from streamlit.logger import get_logger


# PAGES = {
#     "Registration": registration,
#     "Face-Recognition": recognize_faces
# }
# st.sidebar.title('Navigation')
# selection = st.sidebar.radio("Go to", list(PAGES.keys()))
# page = PAGES[selection]
# page.app()

LOGGER = get_logger(__name__)

# Dictionary of apps
DEMOS = OrderedDict(
    [
        ("—", (demos.intro, None)),
        (
            "Registration Page",
            (
                registration,
                """
This app is for registration purpose. Store name, category of residence and image database gets automatically triggered which will be used for face-recognition purposes.  
""",
            ),
        ),
        (
            "Face-Recognition",
            (
                recognize_faces,
                """
Real-time Face-Recognition
""",
            ),
        ),
#         (
#             "Mapping Demo",
#             (
#                 demos.mapping_demo,
#                 """
# This demo shows how to use
# [`st.pydeck_chart`](https://docs.streamlit.io/en/latest/api.html#streamlit.pydeck_chart)
# to display geospatial data.
# """,
#             ),
#         ),

        (
            "View Database",
            (
                show_database,
                """
View all the data that has been stored
""",
            ),
        ),
    ]
)

def run():
    demo_name = st.sidebar.selectbox("Choose a demo", list(DEMOS.keys()), 0)
    demo = DEMOS[demo_name][0]

    if demo_name == "—":
        show_code = False
        st.write("# Welcome to Streamlit! 👋")
    else:
        show_code = st.sidebar.checkbox("Show code", True)
        st.markdown("# %s" % demo_name)
        description = DEMOS[demo_name][1]
        if description:
            st.write(description)
        # Clear everything from the intro page.
        # We only have 4 elements in the page so this is intentional overkill.
        for i in range(10):
            st.empty()

    demo()

    if show_code:
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))


if __name__ == "__main__":
    run()