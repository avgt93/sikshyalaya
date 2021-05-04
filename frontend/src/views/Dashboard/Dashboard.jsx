import React, { useState } from "react";
import Button from "../../components/Button";
import Grid from "@material-ui/core/Grid";
import colorscheme from "../../utils/colors";
import DashboardLayout from "../../components/DashboardLayout";
import NotificationButton from "../../components/NotificationButton";
import "./statics/css/Dashboard.css";

const Dashboard = () => {
	const [clicked, setClicked] = useState(false);
	return (
		<DashboardLayout>
			<div className="root">
				<Grid
					container
					direction="column"
					justify="flex-start"
					alignItems="center"
					wrap="nowrap"
				>
					<Grid item className="topBar">
						<NotificationButton />
					</Grid>
					<Grid item className="botBar">
						<Grid
							container
							direction="row"
							justify="center"
							alignItems="center"
						>
							<Grid item className="leftContainer" xs={4}>
								<Grid
									container
									direction="column"
									justify="center"
									alignItems="center"
									className="xdd"
								>
									<Grid item className="activeClassBoxContainer"></Grid>
									<Grid item className="classResourcesBoxContainer"></Grid>
								</Grid>
							</Grid>
							<Grid item className="middleContainer" xs={4}>
								<div className="discussionBoxContainer"></div>
							</Grid>
							<Grid item className="rightContainer" xs={4}>
								<Grid
									container
									direction="column"
									justify="center"
									alignItems="center"
									className="xdd"
								>
									<Grid item className="postBoxContainer"></Grid>
									<Grid item className="quizBoxContainer"></Grid>
									<Grid item className="tbdBoxContainer"></Grid>
								</Grid>
							</Grid>
						</Grid>
					</Grid>
				</Grid>
			</div>
		</DashboardLayout>
	);
};

export default Dashboard;
