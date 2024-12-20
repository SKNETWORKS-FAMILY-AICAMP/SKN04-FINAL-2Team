import React from "react";
import Sidebar from "../sidebar/Sidebar";

const AdminPage = () => {
  return (
    <div>
      <Sidebar />
      <div style={{ marginLeft: "200px", padding: "20px" }}>
        <h1>관리 페이지</h1>
        {/* Add your admin page content here */}
      </div>
    </div>
  );
};

export default AdminPage;