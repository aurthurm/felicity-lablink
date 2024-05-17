import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import SettingsLayout from "@/components/layouts/settings";
import { useEffect, useState } from "react";
import  { useUrl } from "@/utils"

function GeneralSettings() {
  const [verifyResults, setVerifyResults] = useState(false)
  const [uid, setUid] = useState()
  const [resolveHologicEid, setResolveHologicEid] = useState(false)
  const [submissionLimit, setSubmissionLimit] = useState(250)
  const [clearDataOverDays, setClearDataOverDays] = useState(30)
  const [pollDbEvery, setPollDbEvery] = useState(10)
  const [sleepSeconds, setSleepSeconds] = useState(10)
  const [sleepSubmissionCount, setSleepSubmissionCount] = useState(10) 

  useEffect(() => {
   fetch(useUrl("/link-settings")).then((res) => res.json()).then((payload) => {
      const data = payload[0]
      setUid(data.uid)
      setVerifyResults(data.verify_results)
      setResolveHologicEid(data.resolve_hologic_eid)
      setSubmissionLimit(data.submission_limit)
      setClearDataOverDays(data.clear_data_over_days)
      setPollDbEvery(data.poll_db_every)
      setSleepSeconds(data.sleep_seconds)
      setSleepSubmissionCount(data.sleep_submission_count)
   }).catch((err) => {
     console.error(err)
   })
  }, [fetch])

  const updateSettings = async () => {
    fetch(useUrl(`/link-settings/${uid}`), {
      method: "put",
      headers: {
        "Content-type": "application/json"
      },
      body: JSON.stringify({
        verify_results: verifyResults,
        resolve_hologic_eid: resolveHologicEid,
        submission_limit: submissionLimit,
        clear_data_over_days: clearDataOverDays,
        poll_db_every: pollDbEvery,
        sleep_seconds: sleepSeconds,
        sleep_submission_count: sleepSubmissionCount
      })
    })
  }

  return (
      <SettingsLayout>
        <Card x-chunk="dashboard-04-chunk-2">
          <CardHeader>
            <CardTitle>General Settings</CardTitle>
            <CardDescription>
              Configs specific to the LabLInk functionality.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form className="flex flex-col gap-4">
              <div className="flex items-center space-x-2">
                <Checkbox id="verifyResults"
                checked={verifyResults} 
                onChange={(e) => setVerifyResults((e.target as HTMLInputElement).checked)} 
                 disabled />
                <label
                  htmlFor="verifyResults"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  Automatically Verify Results
                </label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox id="resolveHologic" 
                 checked={resolveHologicEid} 
                 onChange={(e) => setResolveHologicEid((e.target as HTMLInputElement).checked)} 
                 disabled/>
                <label
                  htmlFor="resolveHologic"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  Resolve Hologic EIDs
                </label>
              </div>
              <hr />
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="submissionLimit"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Submission
                  </label>
                <Input
                  id="submissionLimit" 
                  className="col-span-8"
                  type="numer"
                  placeholder="Submission Limit"
                  value={submissionLimit}
                  onChange={(e) => setSubmissionLimit(+e.target.value)}
                />
              </div> 
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="pollDb"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Poll DB <span className="italic text-sm">(min)</span>
                  </label>
                <Input
                  id="pollDb" 
                  className="col-span-8"
                  type="numner"
                  placeholder="Poll DB Every"
                  value={pollDbEvery}
                  onChange={(e) => setPollDbEvery(+e.target.value)}
                />
              </div>
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="clearData"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Clear DB <span className="italic text-sm">(days)</span>
                  </label>
                <Input
                  id="clearData" 
                  className="col-span-8"
                  type="numner"
                  placeholder="Clear data over days?"
                  value={clearDataOverDays}
                  onChange={(e) => setClearDataOverDays(+e.target.value)}
                />
              </div>
              <hr />
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="sleepSeconds"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                   Sleep <span className="italic text-sm">(sec)</span>
                  </label>
                <Input
                  id="sleepSeconds" 
                  className="col-span-8"
                  type="numner"
                  value={sleepSeconds}
                  onChange={(e) => setSleepSeconds(+e.target.value)}
                />
              </div>
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="sleepAfter"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Sleep After <span className="italic text-sm">(sec)</span>
                  </label>
                <Input
                  id="sleepAfter" 
                  className="col-span-8"
                  type="number"
                  placeholder="Sleep after x submissions?"
                  value={sleepSubmissionCount}
                  onChange={(e) => setSleepSubmissionCount(+e.target.value)}
                />
              </div>
            </form>
          </CardContent>
          <CardFooter className="border-t px-6 py-4">
            <Button onClick={() => updateSettings()}>Update</Button>
          </CardFooter>
        </Card>
      </SettingsLayout>
  )
}

export default GeneralSettings
