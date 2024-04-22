import './styles/DivbdSearPRod.css'; // Import the CSS file

import React, { useState, useEffect } from "react";
import axios from 'axios';
import { Navigate } from 'react-router-dom';
import './styles/DivbdSearPRod.css'; // Import the CSS file
import Loader from './Loader';


function DivbdSearPRod() {
    const [result, setResult] = useState(null);
    const [status, setStatus] = useState(null);
    const [redirect, setRedirect] = useState(false);
    const [searchPro, setSearchPro] = useState('');
    const [dataFromAmazon, setDataFromAmazon] = useState([]);
    const [dataFromAliexpress, setDataFromAliexpress] = useState([]);
    const [dataFromEbay, setDataFromEbay] = useState([]);
    const [queryString, setQueryString] = useState('');
    const [loading, setLoading] = useState(false); // Ajout du state pour le chargement

    useEffect(() => {
        console.log("dataFromAmazon:", dataFromAmazon);
        console.log("dataFromAliexpress:", dataFromAliexpress);
        console.log("dataFromEbay:", dataFromEbay);
    }, [dataFromAmazon, dataFromAliexpress, dataFromEbay]);



    function handleFormReact(event) {
        event.preventDefault();
        setLoading(true);
        let api_url = "http://127.0.0.1:8000/api/sear";
        const data = new FormData(event.target);
        axios.post(api_url, data, {
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then((response) => {
            setLoading(false); // Définir le chargement sur false une fois la réponse reçue
            setResult(response.data.message);
            setStatus(response.data.status);
            setDataFromAmazon(response.data.dataFromAmazon);
            setDataFromAliexpress(response.data.dataFromAliexpres);
            setDataFromEbay(response.data.dataFromEbay);
            if (response.data.status === true){
                const queryString = new URLSearchParams({

                    dataFromAmazon: JSON.stringify(response.data.dataFromAmazon),
                    dataFromAliexpress: JSON.stringify(response.data.dataFromAliexpres),
                    dataFromEbay: JSON.stringify(response.data.dataFromEbay)
                }).toString();
                setQueryString(queryString);
                setRedirect(true); // Déclenche la redirection
            }
        })
        .catch((error) => {
            setLoading(false); // Définir le chargement sur false en cas d'erreur
            console.error("Error:", error);
        });
    }

    return(
        <div className="parentdiv" >
            <div className="divSearchPro">
                {/* {redirect && <Navigate to="/scrapage" />} Navigate conditionnelle */}
                {redirect && (
                    <Navigate to={`/scrapage?${queryString}`} />
                )}
                <div>
                    <h1>What product do u have in mind ?</h1>

                </div>

                <div className="divformsearchprod">
                    <form onSubmit={handleFormReact} className="search-bar">
                        <input type="search" name="searchpro" pattern=".*\S.*" required />
                        <button className="search-btn" type="submit">
                            <span>Search</span>
                        </button>
                    </form>   
                    {/*{loading && <p>Loading...</p>} {/* Afficher le message de chargement lorsque loading est true */}  
                    {loading && <Loader />}
                    {result && (
                        <div>
                          <h1>{result}</h1>
                        </div>
                      )}
                </div>
                  
            </div>
        </div>
    )   
}   

export default DivbdSearPRod;


// import './styles/DivbdSearPRod.css'; // Import the CSS file

// import React, { useState, useEffect } from "react";
// import axios from 'axios';
// import { Navigate } from 'react-router-dom';
// import './styles/DivbdSearPRod.css'; // Import the CSS file

// function DivbdSearPRod() {
//     const [result, setResult] = useState(null);
//     const [status, setStatus] = useState(null);
//     const [redirect, setRedirect] = useState(false);
//     const [searchPro, setSearchPro] = useState('');
//     const [dataFromAmazon, setDataFromAmazon] = useState([]);
//     const [dataFromAliexpress, setDataFromAliexpress] = useState([]);
//     const [dataFromEbay, setDataFromEbay] = useState([]);
//     const [queryString, setQueryString] = useState('');
//     const [loading, setLoading] = useState(false); // Ajout du state pour le chargement

//     useEffect(() => {
//         console.log("dataFromAmazon:", dataFromAmazon);
//         console.log("dataFromAliexpress:", dataFromAliexpress);
//         console.log("dataFromEbay:", dataFromEbay);
//     }, [dataFromAmazon, dataFromAliexpress, dataFromEbay]);

//     function handleFormReact(event) {
//         event.preventDefault();
//         setLoading(true); // Définir le chargement sur true lors de la soumission du formulaire
//         let api_url = "http://127.0.0.1:8000/api/sear";
//         const data = new FormData(event.target);
//         axios.post(api_url, data, {
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//         })
//         .then((response) => {
//             setLoading(false); // Définir le chargement sur false une fois la réponse reçue
//             setResult(response.data.message);
//             setStatus(response.data.status);
//             setDataFromAmazon(response.data.dataFromAmazon);
//             setDataFromAliexpress(response.data.dataFromAliexpress);
//             setDataFromEbay(response.data.dataFromEbay);
//             if (response.data.status === true){
//                 const queryString = new URLSearchParams({
//                     dataFromAmazon: JSON.stringify(response.data.dataFromAmazon),
//                     dataFromAliexpress: JSON.stringify(response.data.dataFromAliexpress),
//                     dataFromEbay: JSON.stringify(response.data.dataFromEbay)
//                 }).toString();
//                 setQueryString(queryString);
//                 setRedirect(true); // Déclenche la redirection
//             }
//         })
//         .catch((error) => {
//             setLoading(false); // Définir le chargement sur false en cas d'erreur
//             console.error("Error:", error);
//         });
//     }

//     return(
//         <div className="divSearchPro">
//             {redirect && (
//                 <Navigate to={`/scrapage?${queryString}`} />
//             )}
//             <div>
//                 <h1>What product do u have in mind ?</h1>
//             </div>
//             <div className="divformsearchprod">
//                 <form onSubmit={handleFormReact} className="search-bar">
//                     <input type="search" name="searchpro" pattern=".*\S.*" required />
//                     <button className="search-btn" type="submit">
//                         <span>Search</span>
//                     </button>
//                 </form>
//                 {loading && <p>Loading...</p>} {/* Afficher le message de chargement lorsque loading est true */}
//                 {result && (
//                     <div>
//                         <h1>{result}</h1>
//                     </div>
//                 )}
//             </div>
//         </div>
//     )
// }

// export default DivbdSearPRod;

