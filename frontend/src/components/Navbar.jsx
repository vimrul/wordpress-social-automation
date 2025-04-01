import { Link } from "react-router-dom";

const Navbar = () => (
  <nav className="bg-gray-800 text-white p-4">
    <div className="container mx-auto flex gap-4">
      <Link to="/" className="text-xl font-bold">
        Home
      </Link>
      <Link to="/dashboard" className="text-xl font-bold">
        Dashboard
      </Link>
    </div>
  </nav>
);

export default Navbar;
