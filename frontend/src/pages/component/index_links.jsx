import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './navbar.jsx';
import DivContactComp from '../component/contactDiv'
import Div_body from "../component/divbody.jsx";
import DivbdSearPRod from "../component/divBodySerProd"
import ScrapColleData from '../component/scrapingCollectData'


function Idexlinks() {
    return (
      <BrowserRouter>
        {/* <Navbar /> */}
        <Routes>
          <Route path="/" element={<Div_body />} />
          <Route path="/search_product" element={<DivbdSearPRod />} />
          <Route path="/contact_us" element={<DivContactComp />} />
          <Route path="/scrapage" element={<ScrapColleData />} />
        </Routes>
      </BrowserRouter>
    );
  }
  
  export default Idexlinks;