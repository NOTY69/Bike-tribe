-- Updated SQL schema with IF NOT EXISTS to avoid errors if tables already exist

CREATE TABLE IF NOT EXISTS public.users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  phone TEXT NOT NULL,
  points INTEGER DEFAULT 0,
  total_trips INTEGER DEFAULT 0,
  total_distance INTEGER DEFAULT 0,
  photo TEXT,
  profile_picture INTEGER
);

CREATE TABLE IF NOT EXISTS public.bikes (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  cc INTEGER NOT NULL,
  mileage INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS public.trips (
  id TEXT PRIMARY KEY,
  created_by TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  start_location TEXT NOT NULL,
  destination TEXT NOT NULL,
  date TIMESTAMP NOT NULL,
  end_date TIMESTAMP,
  time TEXT NOT NULL,
  distance INTEGER NOT NULL,
  bike_id TEXT NOT NULL REFERENCES public.bikes(id) ON DELETE CASCADE,
  max_participants INTEGER NOT NULL,
  participants TEXT[] NOT NULL,
  cost_per_person NUMERIC NOT NULL,
  status TEXT CHECK (status IN ('upcoming', 'ongoing', 'completed', 'cancelled')) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.messages (
  id TEXT PRIMARY KEY,
  trip_id TEXT NOT NULL REFERENCES public.trips(id) ON DELETE CASCADE,
  sender_id TEXT NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  type TEXT CHECK (type IN ('text', 'location', 'photo')) NOT NULL,
  timestamp TIMESTAMP NOT NULL
);
