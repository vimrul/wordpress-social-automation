const Dashboard = () => {
  const handleTwitterLogin = () => {
    window.location.href = "http://localhost:8000/auth/twitter";
  };

  return (
    <div className="container mx-auto my-10">
      <h2 className="text-3xl font-bold mb-4">Dashboard</h2>
      <button
        onClick={handleTwitterLogin}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Connect to Twitter
      </button>
    </div>
  );
};

export default Dashboard;
