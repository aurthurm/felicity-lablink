import { useNavigate } from "react-router-dom"
import linkImage from "@/assets/link.jpeg"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

import { useAuthStore } from '@/store/auth';
import { useEffect, useState } from "react"

function LoginPage() {
  const navigate = useNavigate();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() =>{
    if(isAuthenticated) {
      navigate('/');
    }
  },[isAuthenticated])

  const handleLogin = () => {
    useAuthStore.getState().login(username, password);
    navigate('/');
  };

  return (
    <div className="w-full lg:grid lg:min-h-[600px] lg:grid-cols-2 xl:min-h-[800px]">
      <div className="flex items-center justify-center py-12">
        <div className="mx-auto grid w-[350px] gap-6">
          <div className="grid gap-2 text-center">
            <h1 className="text-3xl font-bold">Login</h1>
            <p className="text-balance text-muted-foreground">
              Enter your username below to login to your account
            </p>
          </div>
          <div className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Username</Label>
              <Input
                id="email"
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="grid gap-2">
              <Input id="password" type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)}
                required 
                />
            </div>
            <Button type="submit" className="w-full" onClick={() => handleLogin()}>
              Login
            </Button>
          </div>
        </div>
      </div>
      <div className="hidden bg-muted lg:block">
        <img
          src={linkImage}
          alt="Image"
          className="h-screen max-h-screen w-full object-git dark:brightness-[0.2] dark:grayscale"
        />
      </div>
    </div>
  )
}
export default LoginPage