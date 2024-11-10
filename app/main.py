# main.py
from dash.dependencies import Input, Output
from dash_components import navigationImage, navigationBrand, navigationLink, app_layout
import page_home, page_doe
from app import app

# ============================================= 1 ===============================================
navBarColor         = "black"
# navImage            = navigationImage(imageLocation="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Logo_Bayer.svg/1024px-Logo_Bayer.svg.png")
navImage            = navigationImage(imageLocation="assets/MJ_cat_Charcoal.jpg")
navbarBrand         = navigationBrand(brandName="Tomato Rootstock Seed Drying")
navLink_home        = navigationLink(linkName="Home", hrefName="/home")
# navLink_online_prediction    = navigationLink(linkName="Soft Sensor", hrefName="/online_prediction")
navLink_doe         = navigationLink(linkName="DoE", hrefName="/doe")
# navLink_predict     = navigationLink(linkName="Sensitivity Analysis", hrefName="/prediction")
# navLink_digital     = navigationLink(linkName="Digitalization", hrefName="/digitalization")
# navMenu             = navigationDropdownMedu(menuName="Process Optimization", menuItemName=["GSA", "Scale up"], menuItemHref=["/gsa", "/scale_up"], menuColor=navBarColor)

# ============================================= 2 ===============================================
app.layout = app_layout(
    contents=[
        navImage, navbarBrand, navLink_home, 
        navLink_doe, 
        # navLink_online_prediction,  
        # navLink_database, navLink_model, navLink_predict, navLink_digital
    ],
    navigationBarColor=navBarColor
)

# ============================================= 3 ===============================================
@app.callback(Output("content", "children"),
                [
                    Input("url","pathname")
                ])
def pathname(pathname):
    if pathname == "/home":
        return page_home.layout
    elif pathname == "/doe":
        return page_doe.layout
    else:
        return page_home.layout



# Run the app
if __name__ == "__main__":
    app.run_server("0.0.0.0",port="8080")
    # app.run_server("0.0.0.0",port="8050", debug=True)
