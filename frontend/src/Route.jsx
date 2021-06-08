import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import Login from "./views/Login/LoginBox";
import Dashboard from "./views/Dashboard/Dashboard";
import Notes from "./views/Notes/Notes";
import Landing from "./views/Landing/Landing";
import Quiz from "./views/Quiz/Quiz";
import Profile from "./views/Profile/Profile";
import TeacherDashboard from "./views/TeacherDashboard/TeacherDashboard";
import AdminDashboard from "./views/Admin/AdminDashboard";
import SchoolView from "./views/Admin/SchoolView";
import DepartmentView from "./views/Admin/DepartmentView";
import ProgramView from "./views/Admin/ProgramView";
import GroupView from "./views/Admin/GroupView";
import AdminForm from "./views/Admin/AdminForm";
import StudentView from "./views/Admin/StudentView";
import ResetPassword from "./views/Login/ResetPassword";
import Signup from "./views/Login/Signup";
import StudentRoute from "./components/StudentRoute";
import TeacherRoute from "./components/TeacherRoute";
import AdminRoute from "./components/AdminRoute";
import Verify from "./views/Login/Verify";
import Logout from "./views/Login/Logout";
import QuizCreator from "./views/QuizCreator/QuizCreator";
import NotFound from "./views/404/404";
import ClassSessionCreator from "./views/ClassSessionCreator/ClassSessionCreator";
import configs from "./utils/configs";

const Routes = () => {
  return (
    <Switch>
      <Route exact path="/login" component={Login} />
      <StudentRoute exact path="/class/:classID?" component={Dashboard} />
      <StudentRoute exact path="/quiz" component={Quiz} />
      <StudentRoute exact path="/note" component={Notes} />
      <StudentRoute
        exact
        path="/landing"
        access={configs.USER_TYPES.STUDENT}
        component={Landing}
      />
      <StudentRoute exact path="/profile" component={Profile} />
      <TeacherRoute
        exact
        path="/teacher-dashboard"
        component={TeacherDashboard}
      />
      <AdminRoute exact path="/adminForm" component={AdminForm} />
      <TeacherRoute
        exact
        path="/class-session-create"
        component={ClassSessionCreator}
      />
      <AdminRoute exact path="/admin" component={AdminDashboard} />
      <AdminRoute exact path="/admin/school" component={SchoolView} />
      <AdminRoute
        exact
        path="/admin/department/:school?"
        component={DepartmentView}
      />
      <AdminRoute
        exact
        path="/admin/program/:department?"
        component={ProgramView}
      />
      <AdminRoute exact path="/admin/group/:program?" component={GroupView} />
      <AdminRoute exact path="/admin/student/:group?" component={StudentView} />
      <Route exact path="/reset" component={ResetPassword} />
      <Route exact path="/signup" component={Signup} />
      <Route exact path="/verify" component={Verify} />
      <Route exact path="/logout" component={Logout} />
      <Route exact path="/quiz-creator" component={QuizCreator} />
      <Redirect exact from="/" to="login" />
      <Route exact path="*" component={NotFound} />
    </Switch>
  );
};

export default Routes;
