
// import Scrapitem from "./scrapitem";
// import React from "react";
// import { useLocation } from "react-router-dom";
// import './styles/styledivbody.css'; // Import the CSS file

// function ScrapColleData(){
//     // get from django

//     const location = useLocation();
//     const searchParams = new URLSearchParams(location.search);

//     let parsedDataFromAmazon = [];
//     let parsedDataFromAliexpress = [];
//     let parsedDataFromEbay = [];

//     try {
//         parsedDataFromAmazon = JSON.parse(searchParams.get("dataFromAmazon") || '[]');
//         parsedDataFromAliexpress = JSON.parse(searchParams.get("dataFromAliexpress") || '[]');
//         parsedDataFromEbay = JSON.parse(searchParams.get("dataFromEbay") || '[]');
//     } catch (error) {
//         console.error("Error parsing JSON:", error);
//         // console.log("Error parsing JSON:", error);
//     }

//     console.log("dataFromAmazon:", parsedDataFromAmazon);
//     console.log("dataFromAliexpress:", parsedDataFromAliexpress);
//     console.log("dataFromEbay:", parsedDataFromEbay);

//     return(
//         <div>
//             <div className="result_content">
//             <div className="amazon_data">
//                 <h1>Data from Amazon</h1>
//                 {parsedDataFromAmazon.map((item, index) => {
//                     // console.log("item:", item);
//                     return (
//                         <Scrapitem key={index} {...item} />
//                     );
//                 })}
//             </div>
            

//             <div className="aliexpress_data">
//                 <h1>Data from Aliexpress</h1>
//                 {parsedDataFromAliexpress.map((item, index) => {
//                     return (
//                         <Scrapitem key={index} {...item} />
//                     );
//                 })}
//             </div>

//             <div className="ebay_data">    
//                 <h1>Data from Ebay</h1>
//                 {parsedDataFromEbay.map((item, index) => {
//                     return (
//                         <Scrapitem key={index} {...item} />
//                     );
//                 })} 
//             </div>
//             </div>
//         </div>
//     );
// }

// export default ScrapColleData; 

// scrapingCollectData


import Scrapitem from "./scrapitem";
import React from "react";
import { useLocation } from "react-router-dom";
import './styles/scrapdata.css';
function ScrapColleData(){
    // get from django

    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);

    let parsedDataFromAmazon = [];
    let parsedDataFromAliexpress = [];
    let parsedDataFromEbay = [];

    try {
        parsedDataFromAmazon = JSON.parse(searchParams.get("dataFromAmazon") || '[]');
        parsedDataFromAliexpress = JSON.parse(searchParams.get("dataFromAliexpress") || '[]');
        parsedDataFromEbay = JSON.parse(searchParams.get("dataFromEbay") || '[]');
    } catch (error) {
        console.error("Error parsing JSON:", error);
        // console.log("Error parsing JSON:", error);
    }

    // console.log("dataFromAmazon:", parsedDataFromAmazon);
    // console.log("dataFromAliexpress:", parsedDataFromAliexpress);
    // console.log("dataFromEbay:", parsedDataFromEbay);

    return(
        <div className="CONTAINER">
            <div className="datacontainer a">
                <h1>Amazon Data</h1>
                <div>
                    {parsedDataFromAmazon.map((item, index) => {
                    // console.log("item:", item);
                    return (
                        <Scrapitem key={index} {...item} />
                    );
                })}
                </div>

            </div>
            

            <div className="datacontainer b">
                <h1>Aliexpress Data</h1>
                {parsedDataFromAliexpress.map((item, index) => {
                    return (
                        <Scrapitem key={index} {...item} />
                    );
                })}
            </div>

            <div className="datacontainer c">    
                <h1>Ebay Data</h1>
                {parsedDataFromEbay.map((item, index) => {
                    return (
                        <Scrapitem key={index} {...item} />
                    );
                })} 
            </div>

        </div>
    );
}

export default ScrapColleData;
