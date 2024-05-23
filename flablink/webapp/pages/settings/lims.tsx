import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import SettingsLayout from "@/components/layouts/settings";
import { useEffect, useState } from "react";
import { useUrl } from "@/utils";

function LimsSettings() {
  const [uid, setUid] = useState()
  const [address, setAddress] = useState("")
  const [api_url, setApiUrl] = useState("/senaite/@@API/senaite/v1")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [max_attempts, setMaxAttempts] = useState(10)
  const [attempt_interval, setAttemptInterval] = useState(10)

  useEffect(() => {
    fetch(useUrl("/lims-settings"))
    .then((res) => res.json())
    .then((payload) => {
      const data = payload[0]
      setUid(data.uid);
      setAddress(data.address);
      setApiUrl(data.api_url);
      setUsername(data.username);
      setPassword(data.password);
      setMaxAttempts(data.max_attempts);
      setAttemptInterval(data.attempt_interval);
    })
    .catch((err) => { console.error(err)})
  }, [fetch])

  const  updateSettings = async () => {
    fetch(useUrl(`/lims-settings/${uid}`), {
      method: "put",
      headers: {
        "Content-type": "application/json"
      },
      body: JSON.stringify({
        address,
        api_url,
        username,
        password,
        max_attempts,
        attempt_interval,
        is_active: true
      })
    })
  }

  return (
      <SettingsLayout>
        <Card x-chunk="dashboard-04-chunk-2">
          <CardHeader>
            <CardTitle>LIMS Settings</CardTitle>
            <CardDescription>
              Configs specific to the LIMS connection.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form className="flex flex-col gap-4">
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="address"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Address
                </label>
                <Input
                  id="address" 
                  className="col-span-8"
                  placeholder="Address"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                />
              </div> 
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="apirul"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    API URL
                  </label>
                <Input
                  id="apirul" 
                  className="col-span-8"
                  placeholder="API Path"
                  value={api_url}
                  onChange={(e) => setApiUrl(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="username"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Username
                  </label>
                <Input
                  id="username" 
                  className="col-span-8"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="password"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Password
                  </label>
                <Input
                  id="password" 
                  className="col-span-8"
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="attempts"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Attempts
                  </label>
                <Input
                  id="attempts" 
                  className="col-span-8"
                  type="number"
                  placeholder="Max atttempts"
                  value={max_attempts}
                  onChange={(e) => setMaxAttempts(+e.target.value)}
                />
              </div>
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="interval"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Interval
                  </label>
                <Input
                  id="interval" 
                  className="col-span-8"
                  type="Attempt interval?"
                  placeholder="interval"
                  value={attempt_interval}
                  onChange={(e) => setAttemptInterval(+e.target.value)}
                />
              </div>
              {/* <div className="flex items-center space-x-2">
                <Checkbox id="include" defaultChecked />
                <label
                  htmlFor="include"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  Is Active
                </label>
              </div> */}
            </form>
          </CardContent>
          <CardFooter className="border-t px-6 py-4">
            <Button onClick={() => updateSettings()}>Update</Button>
          </CardFooter>
        </Card>
      </SettingsLayout>
  )
}

export default LimsSettings
