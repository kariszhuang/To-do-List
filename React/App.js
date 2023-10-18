import ButtonTitle from "./button_title";
import ReactDOM from 'react-dom';
import React from 'react';


var titlelists={
"Main title":
[   'Sub Title 1',
    'Sub Title 2',
    'Sub Title 3',
],
"Hello":
    ["Earth",
     "World",
      "Multiverse"],

"My Day":
    ["Sleep", "Eat"],

"Halloween":["Sugar",1,444,"Love you"],
"Birthday":["0613"],


"Abaaba":["Hi","aifd","bye"]

};

function App() {
    return <>

        

        {Object.entries(titlelists).map(([title,subtitle],index)=>
        <ButtonTitle key={index} sublist={subtitle} title={title}/>

        )}
        


        </>

    ;
}

ReactDOM.render(<App />, document.getElementById('react'));
