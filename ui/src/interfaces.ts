export interface Media {
  id: number;
  title: string;
  type: string;
  genre: string | null;
  year: number | null;
  image: string | null;
  details: {
    director: string;
    length: number;
  } | null;
}
