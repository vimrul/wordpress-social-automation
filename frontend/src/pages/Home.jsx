import { useState } from "react";
import PostsList from "../components/PostsList";

const Home = () => {
  const [jsonUrl, setJsonUrl] = useState("");

  return (
    <div className="container mx-auto my-10">
      <h2 className="text-2xl font-bold mb-4">Fetch WordPress Posts</h2>
      <input
        type="text"
        value={jsonUrl}
        onChange={(e) => setJsonUrl(e.target.value)}
        placeholder="Enter WordPress JSON URL"
        className="border p-2 rounded w-full mb-4"
      />
      {jsonUrl && <PostsList jsonUrl={jsonUrl} />}
    </div>
  );
};

export default Home;
