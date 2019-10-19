import React from "react";

import "./NER_Annotate_Styles.css";

class NERVisualizer extends React.Component {
	render() {
		return this.generateHTML(this.props.text, this.props.spans);
	}

	generateHTML(text, spans) {
		let output = [];
		let offset = 0;

		for (let spanIndex = 0; spanIndex < spans.length; spanIndex++) {
			let { label, start, end } = spans[spanIndex];
			label = label.toUpperCase();
			const entity = text.slice(start, end);
			const fragments = text.slice(offset, start).split("\n");
			fragments.forEach((fragment, i) => {
				output.push(fragment);
				if (fragments.length > 1 && i !== fragments.length - 1) output.push(<br />);
			});
			let color = this.intToHSL(this.hashCode(label));
			let cancelSpanClick = false;
			output.push(
				<span
					data-entity={label}
					style={{ background: color }}
					onClick={(e) => {
						if (cancelSpanClick) {
							cancelSpanClick = false;
							return false;
						}
						this.props.cycleSpanLabel(spanIndex);
					}}>
					{entity}
					<button
						onClick={(e) => {
							cancelSpanClick = true;
							// e.preventDefault();
							// e.nativeEvent.stopImmediatePropagation();
							this.props.deleteSpan(spanIndex);
						}}>
						x
					</button>
				</span>
			);
			offset = end;
		}
		const fragments = text.slice(offset, text.length).split("\n");
		fragments.forEach((fragment, i) => {
			output.push(fragment);
			if (fragments.length > 1 && i !== fragments.length - 1) output.push(<br />);
		});
		return output;
	}

	hashCode(str) {
		// java String#hashCode
		var hash = 0;
		for (var i = 0; i < str.length; i++) {
			hash = str.charCodeAt(i) + ((hash << 5) - hash);
		}
		return hash - 100 * str.length;
	}

	intToHSL(i) {
		return "hsla(" + ((i - 400) % 360) + ", 90%, 65%, 1)";
	}
}

export default NERVisualizer;
