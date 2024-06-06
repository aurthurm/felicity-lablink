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
import { useResultTranslationsStore } from "@/store/settings/translation";

function ResultTranslation() {
  const [uid, setUid] = useState(null)
  const [original, setOriginal] = useState("")
  const [translated, setTranslated] = useState("")
  const [reason, setReason] = useState("")

  const resultTranslations = useResultTranslationsStore((state) => state.resultTranslations)
  const addTranslation = useResultTranslationsStore((state) => state.addTranslation)
  const updateTranslation = useResultTranslationsStore((state) => state.updateTranslation)

  const { fetchTranslations } = useResultTranslationsStore()
  
  useEffect(() => {
    fetchTranslations();
  }, [fetch])

  const initEdit = (translation: any) => {
    setUid(translation.uid);
    setOriginal(translation.original);
    setTranslated(translation.translated);
    setReason(translation.reason);
  }
  const clearUpdate = () => {
    setUid(null);
    setOriginal("");
    setTranslated("");
    setReason("");
  }

  const handleTranslation = () => {
    if (!original || !translated) {
      alert("Please fill in all fields")
      return
    }
    if(!uid && resultTranslations.some(obj => obj.original === original)){
      alert("A translation already exists for: " + original)
      return
    }

    if(uid){
      updateTranslation(uid, original, translated, reason)
    } else {
      addTranslation(original, translated, reason)
    }
    clearUpdate()
  }


  return (
    <SettingsLayout>
    <Card x-chunk="dashboard-04-chunk-1">
      <CardHeader>
        <CardTitle>Result Translation</CardTitle>
        <CardDescription>
          Results that need to be translation to another value.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid grid-cols-12 gap-4">
            <div className="col-span-3"><Input  placeholder="Original" value={original} onChange={(e) => setOriginal(e.target.value)}  /></div>
            <div className="col-span-3" ><Input placeholder="Translation" value={translated} onChange={(e) => setTranslated(e.target.value)} /></div>
            <div className="col-span-6" ><Input placeholder="Translation" value={reason} onChange={(e) => setReason(e.target.value)} /></div>
          </div>
          <Button className="mt-2" onClick={() => handleTranslation()}>{!uid ? "Add" : "Update"}</Button>
          <Button className="mt-2 ml-4" variant="outline" onClick={() => clearUpdate()}>Clear</Button>
        </form>
      </CardContent>
      <CardFooter className="border-t px-6 py-4">
        <ScrollArea className="h-72 w-full">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[200px]">Original</TableHead>
                <TableHead>Translated</TableHead>
                <TableHead>Reason</TableHead>
                <TableHead className="w-[100px]">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
                {resultTranslations?.map((resTranlation: any) => (
                  <TableRow key={resTranlation.uid}>
                    <TableCell className="font-semibold">
                      {resTranlation.original}
                    </TableCell>
                    <TableCell>
                      {resTranlation.translated}
                    </TableCell>
                    <TableCell>
                      {resTranlation.reason}
                    </TableCell>
                    <TableCell>
                      <div className="flex justify-between items-center gap-2">
                      <Button onClick={() => initEdit(resTranlation)}>Edit</Button>
                      <ConfirmDialog 
                        variant="destructive"
                        action="Delete"
                        question="Are you sure?"
                        message={`This action will delete ${resTranlation.original} with its translations permanently!`}
                        handleAction={() => useResultTranslationsStore.getState().deleteTranslation(resTranlation.uid)}
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

export default ResultTranslation
