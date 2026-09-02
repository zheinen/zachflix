import { useState, useEffect } from "react";
import { Container, Typography, Card, CardContent, Grid } from "@mui/material";

interface Media {
  id: number;
  title: string;
  type: string;
  genre: string;
  year: number;
}

function App() {
  const [mediaItems, setMediaItems] = useState<Media[] | null>(null);
  const [mediaTotal, setMediaTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [offset, setOffset] = useState<number>(0);

  const limit = 6;
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `http://localhost:8000/media?limit=${limit}&offset=${offset}`,
        );
        if (!response.ok) {
          throw new Error("There was an error");
        }
        const result = await response.json();
        setMediaItems(result.items);
        setMediaTotal(result.total);
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError("Something went wrong");
        }
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [offset]);
  if (loading) {
    return <div>Loading...</div>;
  }
  if (error) {
    return <div>{error}</div>;
  }
  const clickPrevious = () => {
    setOffset(offset - limit);
  };
  const clickNext = () => {
    setOffset(offset + limit);
  };
  return (
    <Container>
      <Typography variant="h3">ZachFlix!</Typography>
      <Grid container spacing={2}>
        {mediaItems
          ? mediaItems.map((item) => {
              return (
                <Grid key={item.id} size={{ xs: 12, md: 6, lg: 4 }}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">{item.title}</Typography>
                    </CardContent>
                  </Card>
                </Grid>
              );
            })
          : null}
      </Grid>
      <div style={{ display: "flex", flexDirection: "row" }}>
        <button onClick={() => clickPrevious()} disabled={offset - limit < 0}>
          Previous
        </button>
        <button
          onClick={() => clickNext()}
          disabled={offset + limit >= mediaTotal}
        >
          Next
        </button>
      </div>
    </Container>
  );
}
export default App;
