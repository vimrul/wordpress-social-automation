import axios from "axios";
import { useEffect, useState } from "react";

const PostsList = ({ jsonUrl }) => {
  const [posts, setPosts] = useState([]);
  const [selectedPosts, setSelectedPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch posts from backend using jsonUrl
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

  // Toggle checkbox state
  const toggleSelectPost = (id) => {
    setSelectedPosts((prev) =>
      prev.includes(id) ? prev.filter((pid) => pid !== id) : [...prev, id]
    );
  };

  // Post selected items to Twitter
  const postToTwitter = () => {
    const selected = posts.filter((p) => selectedPosts.includes(p.id));

    if (selected.length === 0) {
      alert("Please select at least one post.");
      return;
    }

    selected.forEach((post) => {
      axios
        .post("http://localhost:8000/social/twitter", {
          title: post.title,
          seo_description: post.seo_description || post.excerpt,
          link: post.link,
        })
        .then(() => {
          alert(`✅ Posted: ${post.title}`);
        })
        .catch((error) => {
          alert(`❌ Failed to post: ${post.title}\n${error.message}`);
        });
    });
  };

  // Show loading state
  if (loading) {
    return <p className="text-center my-10 text-xl">Loading posts...</p>;
  }

  // Show error if occurred
  if (error) {
    return <p className="text-center text-red-500 my-10">Error: {error}</p>;
  }

  // Render posts
  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
        {posts.map((post) => (
          <div key={post.id} className="border rounded-lg shadow p-4">
            {post.featured_image && (
              <img
                src={post.featured_image}
                alt={post.title || "Post image"}
                className="rounded mb-3"
              />
            )}
            <h3 className="text-lg font-bold">{post.title}</h3>
            <p className="my-2">{post.excerpt}</p>
            <a
              href={post.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              Read More
            </a>
            <div className="mt-3">
              <input
                type="checkbox"
                checked={selectedPosts.includes(post.id)}
                onChange={() => toggleSelectPost(post.id)}
              />
              <span className="ml-2">Select for posting</span>
            </div>
          </div>
        ))}
      </div>

      {selectedPosts.length > 0 && (
        <div className="text-center my-6">
          <button
            onClick={postToTwitter}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg transition duration-200"
          >
            Post {selectedPosts.length} Selected to Twitter
          </button>
        </div>
      )}
    </>
  );
};

export default PostsList;
