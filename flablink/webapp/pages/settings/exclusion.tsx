import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Input } from "@/components/ui/input"
import SettingsLayout from "@/components/layouts/settings";
import ConfirmDialog from "@/components/confirm";
import { useEffect, useState } from "react";
import { useResultExclusionsStore } from "@/store/settings/exclusion";

function ResultExclusion() {
  const [uid, setUid] = useState(null)
  const [result, setResult] = useState("")
  const [reason, setReason] = useState("")

  const resultExclusions = useResultExclusionsStore((state) => state.resultExclusions)
  const addExclusion = useResultExclusionsStore((state) => state.addExclusion)
  const updateExclusion = useResultExclusionsStore((state) => state.updateExclusion)

  const { fetchExclusions } = useResultExclusionsStore()
  
  useEffect(() => {
    fetchExclusions();
  }, [fetch])

  const initEdit = (reason: any) => {
    setUid(reason.uid);
    setResult(reason.result);
    setReason(reason.reason);
  }
  const clearUpdate = () => {
    setUid(null);
    setResult("");
    setReason("");
  }

  const handleExclusion = () => {
    if (!result || !reason) {
      alert("Please fill in all fields")
      return
    }
    if(!uid && resultExclusions.some(obj => obj.result === result)){
      alert("A reason already exists for: " + result)
      return
    }

    if(uid){
      updateExclusion(uid, result, reason)
    } else {
      addExclusion(result, reason)
    }
    clearUpdate()
  }


  return (
    <SettingsLayout>
    <Card x-chunk="dashboard-04-chunk-1">
      <CardHeader>
        <CardTitle>Result Exclusion</CardTitle>
        <CardDescription>
          Results that need to be excluded during interfacing.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid grid-cols-12 gap-4">
            <div className="col-span-4"><Input  placeholder="Resullt" value={result} onChange={(e) => setResult(e.target.value)}  /></div>
            <div className="col-span-8" ><Input placeholder="Reason" value={reason} onChange={(e) => setReason(e.target.value)} /></div>
          </div>
          <Button className="mt-2" onClick={() => handleExclusion()}>{!uid ? "Add" : "Update"}</Button>
          <Button className="mt-2 ml-4" variant="outline" onClick={() => clearUpdate()}>Clear</Button>
        </form>
      </CardContent>
      <CardFooter className="border-t px-6 py-4">
        <ScrollArea className="h-72 w-full">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[200px]">Result</TableHead>
                <TableHead>Reason</TableHead>
                <TableHead className="w-[100px]">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
                {resultExclusions?.map((excl: any) => (
                  <TableRow key={excl.uid}>
                    <TableCell className="font-semibold">
                      {excl.result}
                    </TableCell>
                    <TableCell>
                      {excl.reason}
                    </TableCell>
                    <TableCell>
                      <div className="flex justify-between items-center gap-2">
                      <Button onClick={() => initEdit(excl)}>Edit</Button>
                      <ConfirmDialog 
                        variant="destructive"
                        action="Delete"
                        question="Are you sure?"
                        message={`This action will delete ${excl.result} with its reasons permanently!`}
                        handleAction={() => useResultExclusionsStore.getState().deleteExclusion(excl.uid)}
                      />
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </CardFooter>
    </Card>
    </SettingsLayout>
  )
}

export default ResultExclusion
