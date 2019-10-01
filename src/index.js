import React from "react";
import ReactDOM from "react-dom";

import Toast from "./Toast";
import NERAnnotator from "./NER_Annotator";

class App extends React.Component {
	constructor(props) {
		super(props);
		// Don't call this.setState() here!
		this.state = {
			currentlyFetching: false,
			avalableEntities: [],
			currentExampleHistoryIndex: 0,
			exampleHistory: [],
			visibleToastObj: null
		};
	}

	componentDidMount() {
		this.fetchAvalableEntities();
		this.showNextExample();
		document.addEventListener("keydown", this.handleKeyPress.bind(this), false);
	}

	componentWillUnmount() {
		document.removeEventListener("keydown", this.handleKeyPress.bind(this), false);
	}

	handleKeyPress(event) {
		console.log(event);
		this.setState({ visibleToastObj: null });
		if (event.key === "ArrowRight") {
			this.showNextExample();
		} else if (event.key === "ArrowLeft") {
			this.showPrevExample();
		} else if (event.key === "z" && (event.ctrlKey === true || event.metaKey === true)) {
			this.undo();
		}
	}

	undo() {
		console.log("undoing");
		const exampleHistory = this.state.exampleHistory;
		const exampleHistoryIndex = this.state.currentExampleHistoryIndex;
		const currentExample = exampleHistory[exampleHistoryIndex];

		if (currentExample.undoHistory.length <= 1) return false;

		currentExample.undoHistory.pop();

		this.setState({ exampleHistory: exampleHistory });
	}

	showPrevExample() {
		const currentExampleHistoryIndex = this.state.currentExampleHistoryIndex;
		if (currentExampleHistoryIndex > 0) this.setState({ currentExampleHistoryIndex: currentExampleHistoryIndex - 1 });
	}

	showNextExample(firstRun) {
		if (this.state.currentlyFetching === true) return;
		const exampleHistory = this.state.exampleHistory;
		const currentExampleHistoryIndex = this.state.currentExampleHistoryIndex;
		if (firstRun != true) this.saveAnnotations(exampleHistory[currentExampleHistoryIndex]);
		if (currentExampleHistoryIndex < exampleHistory.length - 1) {
			this.setState({ currentExampleHistoryIndex: currentExampleHistoryIndex + 1 });
		} else {
			this.setState({ currentlyFetching: true });
			this.fetchNextExample().then((obj) => {
				console.log(obj);
				if (obj.NER_Annotate_Message === "No More Examples") {
					alert("All done - No more examples left to annotate.\nEverything is saved. You can close this page now.");
					this.setState({ currentlyFetching: false });
				} else {
					obj.undoHistory = [{ spans: obj.ents }];
					delete obj.ents;
					const newExampleHistory = exampleHistory.concat([obj]);
					this.setState({
						currentlyFetching: false,
						exampleHistory: newExampleHistory,
						currentExampleHistoryIndex: newExampleHistory.length - 1
					});
				}
			});
		}
	}

	fetchNextExample() {
		return fetch("http://localhost:8080/next").then(function(response) {
			return response.json();
		});
	}

	saveAnnotations(example) {
		console.log(example);
		this.showToast("Annotations Saved", "success", 3000);
	}

	fetchAvalableEntities() {
		fetch("http://localhost:8080/avalable_ents")
			.then(function(response) {
				return response.json();
			})
			.then((myJson) => {
				let array = myJson;
				console.log(array);
				this.setState({ avalableEntities: array });
			});
	}

	updateSpans(newSpans) {
		const exampleHistory = this.state.exampleHistory;
		const exampleHistoryIndex = this.state.currentExampleHistoryIndex;
		const currentExample = exampleHistory[exampleHistoryIndex];

		currentExample.undoHistory = currentExample.undoHistory.concat([
			{
				spans: newSpans
			}
		]);

		this.setState({ exampleHistory: exampleHistory });
	}

	render() {
		const exampleHistory = this.state.exampleHistory;
		const exampleHistoryIndex = this.state.currentExampleHistoryIndex;
		const currentExample = exampleHistory[exampleHistoryIndex];

		let loadingElm = null;
		if (this.state.currentlyFetching) loadingElm = <progress id="Fetching_Indicator"></progress>;

		if (currentExample !== undefined) {
			const undoHistory = currentExample.undoHistory;
			const currentUndo = undoHistory[undoHistory.length - 1];

			return (
				<div className="App">
					{loadingElm}
					<NERAnnotator
						text={currentExample.text}
						spans={currentUndo.spans}
						avalableEntities={this.state.avalableEntities}
						updateSpans={this.updateSpans.bind(this)}
					/>
					<Toast
						level={(this.state.visibleToastObj || {})["level"] || ""}
						message={(this.state.visibleToastObj || {})["message"] || ""}
						visible={this.state.visibleToastObj != null}
					/>
				</div>
			);
		} else {
			return "Loading...";
		}
	}

	showToast(message, level, durration) {
		this.setState({
			visibleToastObj: {
				message: message,
				level: level
			}
		});
		setTimeout(() => {
			this.setState({ visibleToastObj: null });
		}, durration);
	}
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);
