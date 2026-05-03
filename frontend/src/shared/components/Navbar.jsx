import { Link } from "react-router-dom";

export default function Navbar({ user, onLogout }) {
  return (
    <header className="navbar">
      <div className="navbar__logo">FRONT</div>

      <nav className="navbar__auth">
        {user ? (
          <>
            <span className="navbar__email">{user.email}</span>
            <button className="navbar__logout" onClick={onLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link className="navbar__link" to="/login">
              Login
            </Link>
            <Link className="navbar__link" to="/register">
              Register
            </Link>
          </>
        )}
      </nav>
    </header>
  );
}