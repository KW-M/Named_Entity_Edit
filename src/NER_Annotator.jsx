import React from "react";
import NERVisualizer from "./NER_Visualizer";

class NERAnnotator extends React.Component {
	constructor(props) {
		super(props);
		// // Don't call this.setState() here!
		this.state = {
			text: props.text || "No Text Given",
			ents: props.avalableEnts || [
				"PRODUCT",
				"ORG",
				"GPE",
				"LOC",
				"MONEY",
				"TIME",
				"PERCENT",
				"DATE",
				"QUANTITY",
				"ORDINAL",
				"CARDINAL",
				"PERSON",
				"NORP",
				"FAC"
			],
			lastEnt: null,
			undoHistory: [
				{
					spans: props.spansObj || []
				}
			]
		};
	}

	componentWillReceiveProps(nextProps) {
		// console.log("componentWillReceiveProps");
		this.setState({
			text: nextProps.text || "No Text Given",
			ents: nextProps.ents || this.state.ents,
			undoHistory: [
				{
					spans: nextProps.spansObj || []
				}
			]
		});
	}

	render() {
		const undoHistory = this.state.undoHistory;
		const current = undoHistory[undoHistory.length - 1];
		console.log(undoHistory);
		return (
			<figure
				id="displacy_container"
				onMouseUp={(e) => {
					this.handleMouseUp(e);
				}}>
				<NERVisualizer
					text={this.state.text}
					ents={this.state.ents}
					spans={current.spans}
					deleteSpan={this.deleteSpan.bind(this)}
					cycleSpanLabel={this.cycleSpanLabel.bind(this)}
				/>
			</figure>
		);
	}

	undo() {
		console.log("undoing");
		if (this.state.undoHistory.length <= 1) return false;
		// console.log("pre", this.state.undoHistory);
		// console.log("post", this.state.undoHistory.slice(0, this.state.undoHistory.length - 1));
		this.setState({
			undoHistory: this.state.undoHistory.slice(0, this.state.undoHistory.length - 1)
		});
	}

	deleteSpan(spanIndex) {
		// console.log("sel", spanIndex);
		const undoHistory = this.state.undoHistory;
		const current = undoHistory[undoHistory.length - 1];
		const spans = current.spans.slice();
		// console.log(spans);
		spans.splice(spanIndex, 1);
		// console.log(spans);
		this.setState({
			undoHistory: undoHistory.concat([
				{
					spans: spans
				}
			])
		});
	}

	cycleSpanLabel(spanIndex) {
		const undoHistory = this.state.undoHistory;
		const current = undoHistory[undoHistory.length - 1];
		const spans = current.spans.slice();
		spans[spanIndex] = {
			start: spans[spanIndex].start,
			end: spans[spanIndex].end,
			label: this.state.ents[(this.state.ents.indexOf(spans[spanIndex].label) + 1) % this.state.ents.length]
		};
		this.setState({
			undoHistory: undoHistory.concat([
				{
					spans: spans
				}
			])
		});
	}

	componentDidMount() {
		document.addEventListener("keydown", this.handleKeyPress.bind(this), false);
	}

	componentWillUnmount() {
		document.removeEventListener("keydown", this.handleKeyPress.bind(this), false);
	}

	handleKeyPress(event) {
		console.log(event);
		if (event.key === "z" && (event.ctrlKey === true || event.metaKey === true)) this.undo();
	}

	handleMouseUp(e) {
		const undoHistory = this.state.undoHistory;
		const current = undoHistory[undoHistory.length - 1];
		var spans = current.spans.slice();
		var selection = this.getSelectionRange();

		if (selection.start === selection.end) return false;

		var { spans, selection } = this.findSpansOverlapingSelection(spans, selection);
		console.log("selection: " + this.state.text.slice(selection.start, selection.end), selection);

		selection["label"] = this.state.ents[0];
		console.log(spans, selection);

		let spanIndex = 0;
		while (spans[spanIndex] && spans[spanIndex].end < selection.start) spanIndex++;
		if (spanIndex >= spans.length) spans.push(selection);
		else spans.splice(spanIndex, 0, selection);

		this.setState({
			undoHistory: undoHistory.concat([
				{
					spans: spans
				}
			])
		});
	}

	findSpansOverlapingSelection(spans, selection) {
		for (let spanIndex = 0; spanIndex < spans.length; spanIndex++) {
			let span = spans[spanIndex];
			if (
				selection.start <= span.end &&
				span.end <= selection.end &&
				(selection.start <= span.start && span.start <= selection.end)
			) {
				console.log("splicing", spans[spanIndex]);
				spans.splice(spanIndex, 1);
				spanIndex--;
			} else if (selection.start <= span.start && span.start <= selection.end) {
				console.log("trimming end to: " + (span.end + 1), spans[spanIndex]);
				selection.end = span.start;
			} else if (selection.start <= span.end && span.end <= selection.end) {
				console.log("trimming start to: " + (span.end + 1), spans[spanIndex]);
				selection.start = span.end;
			} else {
				console.log("not splicing", spans[spanIndex]);
			}
		}
		return { spans: spans, selection: selection };
	}

	getSelectionRange() {
		let windowSelection = window.getSelection();
		if (windowSelection.rangeCount === 0) return { start: 0, end: 0 };
		let startRange = windowSelection.getRangeAt(0);
		console.log(startRange);
		let endRange = windowSelection.getRangeAt(windowSelection.rangeCount - 1);
		console.log(endRange);
		let start = 0;
		let end = 0;
		let charcounter = 0;

		document.getElementById("displacy_container").childNodes.forEach((element) => {
			// console.dir(element);
			if (element === startRange.startContainer || element === startRange.startContainer.parentNode) {
				start = charcounter + startRange.startOffset;
			}
			if (element === endRange.endContainer || element === endRange.endContainer.parentNode) {
				end = charcounter + endRange.endOffset;
				return;
			}
			if (element.nodeName === "BR") {
				charcounter += 1;
				console.log("here");
			} else if (element.nodeType === 1 && element.hasAttribute("data-entity")) {
				charcounter -= 1;
			}
			charcounter += element.textContent.length;
		});
		windowSelection.removeAllRanges();
		return { start: start, end: end };
	}
}

export default NERAnnotator;
