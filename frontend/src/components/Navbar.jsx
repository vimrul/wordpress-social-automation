import { Link } from "react-router-dom";

const Navbar = () => (
  <nav className="bg-gray-800 text-white p-4">
    <div className="container mx-auto">
      <Link to="/" className="text-xl font-bold">
        Social Automation Dashboard
      </Link>
    </div>
  </nav>
);

export default Navbar;
