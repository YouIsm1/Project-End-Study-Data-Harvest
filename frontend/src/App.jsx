import { useState } from 'react';
import HeaderComp from './pages/component/headercomponent.jsx';
import Idexlinks from './pages/component/index_links.jsx';
import './appstyling.css';

// import backgroundImage from './assets/background0.png';  // Import the image
// import backgroundGif from './assets/background_gif.gif'; // Import the GIF


function App() {

  return (
    <div className='main' >
      <HeaderComp />
      
      <div className="content">
        <Idexlinks />
      </div>
    </div>  
  )
}

export default App
