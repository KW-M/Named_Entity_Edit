import React from "react";

import "./Toast_Styles.css";

class Toast extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			visible: false
		};
	}

	render() {
		let classes = `toast ${this.props.level} `;
		classes += this.state.visible ? "visible" : "";
		return (
			<div className={classes}>
				<p>{this.props.message}</p>
			</div>
		);
	}
	componentWillReceiveProps(nextProps) {
		if (this.props.visible !== nextProps.visible) {
			this.setState({
				visible: nextProps.visible
			});
		}
	}
}

export default Toast;
