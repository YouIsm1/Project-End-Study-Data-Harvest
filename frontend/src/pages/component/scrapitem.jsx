import React, { useState } from "react";
import './styles/scrapeditems.css';

function Scrapitem(props) {
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    return (
        <div  className="totdata">

            <div className="productinfos">
                <div className="scrapedData">
                    <div className="container_images">
                        <div className="images">
                            <div className="img">
                            </div>
                                {props.image_table && props.image_table.length > 0 && props.image_table.map((image, index) => (
                                    <img key={index} src={image} alt={`product_image_${index}`} />
                                ))}
                            {/* </div> */}
                        </div>
                    </div>
                    <div className="infosprod">
                        <div className="name">
                            <h3>{props.name && <span>{props.name}</span>}</h3>
                        </div>
                        <div className="priceprod">
                            <h4>{props.price && <span>The price : {props.price}</span>} $</h4>
                        </div>
                        {/* description sous form dyal table  */}
                        <div className="descp">
                            {props.description ? (
                                <table>
                                <tbody>
                                    {Array.isArray(props.description) ? (
                                    props.description.map((item, index) => (
                                        <tr key={index}>
                                        <th>{item.label}</th>
                                        <td>{item.value}</td>
                                        </tr>
                                    ))
                                    ) : (
                                    <tr>
                                        <td colSpan="2">{props.description}</td>
                                    </tr>
                                    )}
                                </tbody>
                                </table>
                            ) : (
                                <p className="descrpara">{props.description}</p>
                            )}
                            </div>

                    </div>
                </div>
            </div>
            <div className="reviewsclients">
                <h2>clients reviews</h2>
                <div className="statistiqu">
                    <div className="totdata">
                        <div className="negtidonne">
                            <div className="nbrcommtneg">
                                {props.info_comment_Sent.dicNegt && props.info_comment_Sent.dicPost &&(
                                    <h4>The pourcentage of the negative comments  is : {(props.info_comment_Sent.dicNegt.nbrComNegt * 100) / (props.info_comment_Sent.dicNegt.nbrComNegt + props.info_comment_Sent.dicPost.nbrComPost)} %</h4>
                                )}
                            </div>
                            <div className="exemplecomment">
                                <h4>Comments examples :</h4>
                                <div className="commentaires">
                                    {props.info_comment_Sent.dicNegt && props.info_comment_Sent.dicNegt.listCommNegt.slice(0, 3).map((comment, index) => (
                                        <p key={index}>{comment}</p>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <div className="postfdonne negtidonne">
                        <div className="nbrcommtneg">
                                {props.info_comment_Sent.dicPost && props.info_comment_Sent.dicNegt &&(
                                    <h4>The pourcentage of positive comments  is : {(props.info_comment_Sent.dicPost.nbrComPost * 100) / (props.info_comment_Sent.dicNegt.nbrComNegt + props.info_comment_Sent.dicPost.nbrComPost)} %</h4>
                                )}
                            </div>
                            <div className="exemplecomment">
                                <h4>Comments examples</h4>
                                <div className="commentaires">
                                    {props.info_comment_Sent.dicPost && props.info_comment_Sent.dicPost.listCommPost.slice(0, 3).map((comment, index) => (
                                        <p key={index}>{comment}</p>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
}

export default Scrapitem;



