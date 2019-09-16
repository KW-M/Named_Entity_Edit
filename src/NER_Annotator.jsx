import React from "react";
import NERVisualizer from "./NER_Visualizer";

class NERAnnotator extends React.Component {
	constructor(props) {
		super(props);
		this.lastUsedEntity = null;
	}
	render() {
		return (
			<figure
				id="ner_visualizer_container"
				onMouseUp={(e) => {
					this.handleMouseUp(e);
				}}>
				<NERVisualizer
					text={this.props.text}
					avalableEntities={this.props.avalableEntities}
					spans={this.props.spans}
					deleteSpan={this.deleteSpan.bind(this)}
					cycleSpanLabel={this.cycleSpanLabel.bind(this)}
				/>
			</figure>
		);
	}

	deleteSpan(spanIndex) {
		const spans = this.props.spans.slice();
		spans.splice(spanIndex, 1);
		this.props.updateSpans(spans);
	}

	cycleSpanLabel(spanIndex) {
		const spans = this.props.spans.slice();
		const avalableEntities = this.props.avalableEntities;

		const newLabel =
			avalableEntities[(avalableEntities.indexOf(spans[spanIndex].label) + 1) % avalableEntities.length] ||
			"No avalable Entities provided";
		this.lastUsedEntity = newLabel;

		spans[spanIndex] = {
			start: spans[spanIndex].start,
			end: spans[spanIndex].end,
			label: newLabel
		};
		this.props.updateSpans(spans);
	}

	handleMouseUp(e) {
		var spans = this.props.spans.slice();
		var selection = this.getSelectionRange();

		if (selection.start === selection.end) return false;

		var { spans, selection } = this.findSpansOverlapingSelection(spans, selection);
		console.log("selection: " + this.props.text.slice(selection.start, selection.end), selection);

		selection["label"] = this.lastUsedEntity || this.props.avalableEntities[0] || "No avalable Entities provided";
		console.log(spans, selection);

		let spanIndex = 0;
		while (spans[spanIndex] && spans[spanIndex].end < selection.start) spanIndex++;
		if (spanIndex >= spans.length) spans.push(selection);
		else spans.splice(spanIndex, 0, selection);

		this.props.updateSpans(spans);
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

		document.getElementById("ner_visualizer_container").childNodes.forEach((element) => {
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
