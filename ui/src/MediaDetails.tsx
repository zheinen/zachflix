import {
  Button,
  CardMedia,
  Grid,
  Typography,
  Stack,
  Chip,
} from "@mui/material";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import type { Media } from "./interfaces";

function MediaDetails() {
  const { id } = useParams();
  const [media, setMedia] = useState<Media | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://localhost:8000/media/${id}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        return response.json();
      })
      .then((data) => setMedia(data))
      .catch((error) => {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError("Something went wrong");
        }
      });
  }, [id]);
  if (error !== null) {
    return <Typography>Error: {error}</Typography>;
  }
  if (media === null) {
    return <Typography>Loading...</Typography>;
  }
  return (
    <>
      <Button onClick={() => navigate("/")}>Back to Collection</Button>
      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <CardMedia
            component={"img"}
            image={media.image ?? undefined}
            alt={media.title}
            sx={{
              width: "100%",
              maxHeight: 500,
              objectFit: "contain",
            }}
          />
        </Grid>
        <Grid size={{ xs: 12, md: 8 }}>
          <Stack spacing={2}>
            <Typography variant="h3">{media?.title}</Typography>

            <Stack direction="row" spacing={1}>
              <Chip label={media.type} />
              <Chip label={media.genre} />
              <Chip label={media.year} />
            </Stack>

            {media.type == "Movie" && (
              <>
                <Typography>Director: {media.details?.director}</Typography>

                <Typography>
                  Runtime: {media.details?.length} minutes
                </Typography>
              </>
            )}
          </Stack>
        </Grid>
      </Grid>
    </>
  );
}

export default MediaDetails;
