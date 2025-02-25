import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    ph_no: "",
    roll_no: "",
    dept: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:8000/api/signup/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    if (response.ok) {
      alert("Signup successful!");
      navigate("/login"); // Redirect to login page
    } else {
      alert(data.error || "Signup failed");
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
        <input type="text" name="ph_no" placeholder="Phone Number" onChange={handleChange} required />
        <input type="text" name="roll_no" placeholder="Roll No" onChange={handleChange} required />
        <input type="text" name="dept" placeholder="Department" onChange={handleChange} required />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default Signup;
