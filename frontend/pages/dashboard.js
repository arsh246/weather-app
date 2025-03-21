import { useEffect, useState } from "react";
import { auth } from "../lib/firebase";
import { onAuthStateChanged, signOut } from "firebase/auth";
import { useRouter } from "next/router";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (!currentUser) {
        router.push("/login"); // Redirect to login if not authenticated
      } else {
        setUser(currentUser);
      }
    });

    return () => unsubscribe();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      {user ? <p>Welcome, {user.email}!</p> : <p>Loading...</p>}
      <button onClick={() => signOut(auth)}>Logout</button>
    </div>
  );
}
