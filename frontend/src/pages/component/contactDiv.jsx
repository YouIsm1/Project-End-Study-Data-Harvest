import React, { useState } from 'react';
import axios from 'axios';
import './styles/feedback.css'

function DivContactComp() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        message: '',
        subject: ''
    });

    const handleMessageContact = (event) => {
        event.preventDefault();
        let api_url = "http://127.0.0.1:8000/api/SendEmail";
        axios.post(api_url, formData)
            
            .then((response) => {
                alert(response.data.message);
            })
            .catch((error) => {
                console.error("Error:", error);
            });
            
        setFormData({
            username: '',
            email: '',
            message: '',
            subject: ''
        });
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    return (
        <div className="contact_div">
            <div className="contact_container">
                <div>
                    <div className="head_conatct_container">
                        <h2>Send us a feedback ? </h2>
                    </div>
                    <div className="form_contact_container">


                        <form onSubmit={handleMessageContact} className="clas_form_contact">
                            <input name="username" type="text" class="feedback-input" placeholder="Name" value={formData.username} onChange={handleChange}/>   
                            <input name="subject" type="text" class="feedback-input" placeholder="Subject" value={formData.subject} onChange={handleChange} />   

                            <input name="email" type="text" class="feedback-input" placeholder="Email"  value={formData.email} onChange={handleChange}/>
                            <textarea name="message" class="feedback-input" placeholder="Comment" value={formData.message} onChange={handleChange} ></textarea>
                            <input type="submit" value="SUBMIT"/>

                            <div className="submitionMeassage">
                                {/* <div className="footer_contact_container">
                                    <h5>Thank you for your message ! </h5>
                                    <h5>wanna retry ? </h5>

                                </div> */}
                                <button name="btn_res" type="reset" onClick={() => setFormData({
                                    username: '',
                                    email: '',
                                    message: '',
                                    subject: ''
                                })}>reset</button>
                            </div>

                        </form>

                    </div>
                            
                </div>
            </div>
        </div>
    )
}

export default DivContactComp;
