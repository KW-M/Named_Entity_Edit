import React from "react";
import ReactDOM from "react-dom";

import NERAnnotator from "./NER_Annotator";

class App extends React.Component {
	constructor(props) {
		super(props);
		// // Don't call this.setState() here!
		this.state = { text: "Loading...", spans: [], databaseId: null };
	}

	componentDidMount() {
		this.getNext();
	}

	getNext() {
		fetch("http://127.0.0.1:8080/next")
			.then(function(response) {
				return response.json();
			})
			.then((myJson) => {
				let obj = myJson;
				console.log(obj);
				this.setState({ text: obj.text || "error", spans: obj.ents || [], databaseId: obj.database_id || "" });
				// this.forceUpdate();
			});
	}

	render() {
		return (
			<div className="App">
				{/* {JSON.stringify(this.state)} */}
				{/* <h1>Hello CodeSandbox</h1> */}
				<NERAnnotator text={this.state.text} spansObj={this.state.spans} />
			</div>
		);
	}
}

//     parse(text = this.defaultText, model = this.defaultModel, ents = this.defaultEnts) {
//         if(labelof this.onStart === 'function') this.onStart();

//         let xhr = new XMLHttpRequest();
//         xhr.open('POST', this.api, true);
//         xhr.setRequestHeader('Content-label', 'text/plain');
//         xhr.onreadystatechange = () => {
//             if(xhr.readyState === 4 && xhr.status === 200) {
//                 if(labelof this.onSuccess === 'function') this.onSuccess();
//
//             }

//             else if(xhr.status !== 200) {
//                 if(labelof this.onError === 'function') this.onError(xhr.statusText);
//             }
//         }

//         xhr.onerror = () => {
//             xhr.abort();
//             if(labelof this.onError === 'function') this.onError();
//         }

//         xhr.send(JSON.stringify({ text, model }));
//     }

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
