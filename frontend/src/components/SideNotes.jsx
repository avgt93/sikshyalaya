import React, { useState } from "react";
import { Formik, Field, Form } from "formik";
import { Route, Switch, Redirect } from "react-router-dom";
import Button from "../components/Button";
import * as yup from "yup";
import Tab from "../components/Tab";
import Grid from "@material-ui/core/Grid";
import Image from "../components/Image";
import profile from "../assets/pp.jpg";
import SideBar from "../components/SideBar";
import colorscheme from "../utils/colors";
import ProfileBar from "../components/ProfileBar";
import DashboardLayout from "../components/DashboardLayout";
import { ImCross } from "react-icons/im";
import { FiTrash } from "react-icons/fi";

const styleSheet = {
  root: {
    flexGrow: "1",
    width: "350px",
    height: "220px",
    background: colorscheme.white,
    borderRadius: "20px",
    boxShadow: "2px 2px 10px -3px rgba(0,0,0,0.2)",
    cursor: "pointer",
    color: colorscheme.black,
  },
  innerContainer: {
    overflow: "hidden",
    height: "80%",
    position: "relative",
    top: "8%",
  },
  titleTextContainer: {
    fontWeight: "bold",
    fontSize: "1.4em",
    position: "relative",
    top: "12%",
    left: "7%",
    width: "85%",
    maxHeight: "30%",
  },
  contentTextContainer: {
    width: "80%",
    position: "relative",
    top: "8px",
    left: "7%",
    wordWrap: "normal",
    textAlign: "justify",
    lineHeight: "1.7em",
  },
};

const SideNotes = ({ title, content, onClick, ...rest }) => {
  return (
    <Grid
      container
      direction="column"
      style={styleSheet.root}
      onClick={onClick}
    >
      <Grid item style={styleSheet.innerContainer}>
        <Grid
          container
          direction="column"
          alignItems="flex-start"
          wrap="nowrap"
        >
          <Grid item style={styleSheet.titleTextContainer}>
            <a style={styleSheet.titleText}>{title}</a>
          </Grid>
          <Grid item style={styleSheet.contentTextContainer}>
            <a style={styleSheet.contentText}>{content}</a>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default SideNotes;
