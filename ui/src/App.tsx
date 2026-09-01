import { useState, useEffect } from "react";

interface Media {
  id: number;
  title: string;
  type: string;
  genre: string;
  year: number;
}

function App() {
  const [media, setMedia] = useState<Media[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch("http://localhost:8000/media");
        if (!response.ok) {
          throw new Error("There was an error");
        }
        const result = await response.json();
        setMedia(result);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);
  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>ZachFlix!</h1>
      <ul>
        {media
          ? media.map((item) => <li key={item.id}>{item.title}</li>)
          : null}
      </ul>
    </div>
  );
}
export default App;
