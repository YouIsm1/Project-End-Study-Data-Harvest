import React from "react";
import './styles/styledivbody.css';
import background_vid5 from '../../assets/background_vid5.mp4'

function Div_body(){

    return(
        

        <div className="homebody">
            <div className="overlay">
      <video src={background_vid5} autoPlay loop muted />
      </div>
            <div className="homebody1">
            <h1>Unearth Insights, Reap Knowledge! Welcome to Data Harvest</h1>

            </div>
            
            <div className="homebody2">
                <h2>Hey ! </h2>
                <div className="descrip">
                    <p>
                    An innovative platform! Our main goal is to provide users with an advanced search experience by allowing them to compare, choose, 
                    and pick one of the many products we're offering. With our intuitive search functionality, 
                    users can easily find the products they're looking for and access detailed information,
                    pricing, and reviews all in one place. Whether you're searching for the latest gadgets, 
                    fashion items, home essentials, or anything in between, our platform empowers users 
                    to make informed decisions and discover the perfect product that suits their needs and preferences.
                    Welcome to a new era of online shopping where convenience, choice, and confidence converge!</p>
                </div>
            </div>
        </div>
    )
}

export default Div_body