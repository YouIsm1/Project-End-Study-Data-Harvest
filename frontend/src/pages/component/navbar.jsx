import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Outlet, Link } from "react-router-dom";
// import Home_page from "../pagespages/pagehome.jsx";

import './styles/navbar.css';

function Navbar() {
  return (
    <nav>
      <div className="wrapper">
        <div className="logo">
        <h2>DATA HARVEST</h2>

        </div>

        <input type="radio" name="slider" id="menu-btn" />
        <input type="radio" name="slider" id="close-btn" />
        <ul className="nav-links">
          <label htmlFor="close-btn" className="btn close-btn"><i className="fas fa-times"></i></label>
          <li><a href="/">Home</a></li>
          <li><a href="/search_product">Test a product</a></li>
          
          
          <li><a href="/contact_us">Feedback</a></li>
        </ul>
        <label htmlFor="menu-btn" className="btn menu-btn"><i className="fas fa-bars"></i></label>
      </div>
    </nav>
  );
}

export default Navbar;


// function Navbar(){
{/* <li>
            <a href="#" className="desktop-item">Mega Menu</a>
            <input type="checkbox" id="showMega" />
            <label htmlFor="showMega" className="mobile-item">Mega Menu</label>
            <div className="mega-box">
              <div className="content">
                <div className="row">
                  <img src="https://avatars.githubusercontent.com/u/128047189?v=4" alt="" />
                  <div className="profile-links">
                  <ul>
                    <li><a href="#"><i class="fa fa-linkedin"></i> LinkedIn</a></li>
                    <li><a href="#"><i class="fa fa-github"></i> Github</a></li>
                    <li><a href="#"><i class="fa fa-instagram"></i> Instagram</a></li>
                  </ul> </div>
                </div>
                {/* Rest of your mega menu content */}
              
    

//     return(
//         <nav>
//             <div class="wrapper">
//                 <div className="logo"><img src={require("C:/Users/hp/Desktop/PFE/PFE_Frontend_Backend-main/pfetest1/frontend/src/pages/component/imgs/logo.jpeg")} alt="Logo" /></div>
//                 <input type="radio" name="slider" id="menu-btn" />
//                 <input type="radio" name="slider" id="close-btn" />

                
//                         <nav>
//                             <ul className="nav-links">
                                
//                                 <li>
//                                     <Link to="/">Home</Link>
//                                 </li>
//                                 <li>
//                                     <Link to="/search_product">search product</Link>
//                                 </li>
//                                 <li>
//                                     <Link to="/contact_us">Contact us</Link>
//                                 </li>
//                             </ul>
//                         </nav>
//             </div>
//         </nav>
//     )
// }

// export default Navbar