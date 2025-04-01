import axios from "axios";
import { useEffect, useState } from "react";

const PostsList = ({ jsonUrl }) => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get(`http://localhost:8000/wordpress/posts?json_url=${jsonUrl}`)
      .then((res) => {
        setPosts(res.data.posts);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [jsonUrl]);

  if (loading)
    return <p className="text-center my-10 text-xl">Loading posts...</p>;

  if (error)
    return <p className="text-center text-red-500 my-10">Error: {error}</p>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
      {posts.map((post) => (
        <div key={post.id} className="border rounded-lg shadow p-4">
          {post.featured_image && (
            <img
              src={post.featured_image}
              alt={post.title}
              className="rounded mb-3"
            />
          )}
          <h3 className="text-lg font-bold">{post.title}</h3>
          <p className="my-2">{post.excerpt}</p>
          <a
            href={post.link}
            target="_blank"
            className="text-blue-500 hover:underline"
          >
            Read More
          </a>
        </div>
      ))}
    </div>
  );
};

export default PostsList;
