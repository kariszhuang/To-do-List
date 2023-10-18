import React, { useState } from "react";
import "./button.css";
function ButtonTitle(props) {
    const [showSubTitles, setShowSubTitles]=useState(false);
  
    const subTitles = props.sublist;
  
    return (
        <div className="buttonContainer">
            <button className="titleButton" onClick={() => setShowSubTitles(!showSubTitles)}>
                {props.title||"Main Title"}
            </button>   
            {showSubTitles && (
              <div style={{position:"absolute"}} className="subtitles">
                    {subTitles.map((subTitle, index) => (
                        <div key={index} className="subTitle" >
                            {subTitle}
                        </div>
                    ))}
             </div>
            )}
        </div>
    );
  }
  
  
export default ButtonTitle;