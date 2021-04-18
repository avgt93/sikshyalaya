import React, { useState } from "react";
import { Formik, Field, Form } from "formik";
import { Route, Switch, Redirect } from "react-router-dom";
import Button from "../../components/Button";
import * as yup from "yup";
import Tab from "../../components/Tab";
import Grid from "@material-ui/core/Grid";
import Image from "../../components/Image";
import profile from "../../assets/pp.jpg";
import SideBar from "../../components/SideBar";
import colorscheme from "../../utils/colors";
import ProfileBar from "../../components/ProfileBar";
import DashboardLayout from "../../components/DashboardLayout";
import Note from "../../components/Note";

const styleSheet = {
	root: {
		flexGrow: "1",
	 	width: "95%",
		margin: "0px auto",
		position: "relative",
		left: "37%",
		top:"15.5%",
	},
};
const typing = true;
const note = {
	title: "hello hi there",
	content: "loresaddsaasjdhkjashdkhaskdjhkajshdkjhakdjskaasdddddddjsd",
	state: typing?"Typing...":"Saved",
}
const Dashboard = () => {
	const [typing,setTyping] =useState(false)
	return (<DashboardLayout>
		<Grid container
			direction="column"
			justify="center"
			alignItems="flex-start"
			style={styleSheet.root}
			spacing={10}
			>
			<Note title={note.title} content={note.content} />
			</Grid>
	</DashboardLayout>);
};

export default Dashboard;
