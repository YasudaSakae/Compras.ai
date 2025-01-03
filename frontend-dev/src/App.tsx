// import Main from "./view/main";
import { Login } from "./view/loginPage/Login";
// import { Register } from "./view/loginPage/Register";
import "./App.css";
import { useContext } from "react";
import { GlobalContext } from "./context/GlobalContext";
import Main from "./view/main";
function App() {
  const { currentPage } = useContext(GlobalContext);
  function renderPage() {
    switch (currentPage) {
      case "login":
        return <Login />;
      // case "register":
      //   return <Register />;
      case "main":
        return <Main />;
      default:
        return <Login />;
    }
  }

  return renderPage();
}

export default App;
