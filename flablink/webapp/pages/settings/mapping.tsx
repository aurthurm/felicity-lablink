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
import { useKeywordMappingsStore } from "@/store/settings/mapping";

function KeywordMapping() {
  const [uid, setUid] = useState(null)
  const [keyword, setKeyword] = useState("")
  const [mappings, setMappings] = useState("")

  const keywordMappings = useKeywordMappingsStore((state) => state.keywordMappings)
  const addMapping = useKeywordMappingsStore((state) => state.addMapping)
  const updateMapping = useKeywordMappingsStore((state) => state.updateMapping)

  const { fetchMappings } = useKeywordMappingsStore()
  
  useEffect(() => {
    fetchMappings();
  }, [fetch])

  const initEdit = (kMapping: any) => {
    setUid(kMapping.uid);
    setKeyword(kMapping.keyword);
    setMappings(kMapping.mappings);
  }
  const clearUpdate = () => {
    setUid(null);
    setKeyword("");
    setMappings("");
  }

  const handleMapping = () => {
    if (!keyword || !mappings) {
      alert("Please fill in all fields")
      return
    }
    if(!uid && keywordMappings.some(obj => obj.keyword === keyword)){
      alert("Keyword already exists. Cannot add new")
      return
    }

    if(uid){
      updateMapping(uid, keyword, mappings)
    } else {
      addMapping(keyword, mappings)
    }
    clearUpdate()
  }


  return (
    <SettingsLayout>
    <Card x-chunk="dashboard-04-chunk-1">
      <CardHeader>
        <CardTitle>KeyWord Mappings</CardTitle>
        <CardDescription>
          Map Instrument Test Codes to be LIMS KeyWords for service identification in LIMS.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid grid-cols-12 gap-4">
            <div className="col-span-4"><Input  placeholder="Test Code" value={keyword} onChange={(e) => setKeyword(e.target.value)}  /></div>
            <div className="col-span-8" ><Input placeholder="Keywords Mappings" value={mappings} onChange={(e) => setMappings(e.target.value)} /></div>
          </div>
          <Button className="mt-2" onClick={() => handleMapping()}>{!uid ? "Add" : "Update"}</Button>
          <Button className="mt-2 ml-4" variant="outline" onClick={() => clearUpdate()}>Clear</Button>
        </form>
      </CardContent>
      <CardFooter className="border-t px-6 py-4">
        <ScrollArea className="h-72 w-full">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[200px]">Test Code</TableHead>
                <TableHead>Keywords Mappings</TableHead>
                <TableHead className="w-[100px]">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
                {keywordMappings?.map((mapping: any) => (
                  <TableRow key={mapping.uid}>
                    <TableCell className="font-semibold">
                      {mapping.keyword}
                    </TableCell>
                    <TableCell>
                      {mapping.mappings}
                    </TableCell>
                    <TableCell>
                      <div className="flex justify-between items-center gap-2">
                      <Button onClick={() => initEdit(mapping)}>Edit</Button>
                      <ConfirmDialog 
                        variant="destructive"
                        action="Delete"
                        question="Are you sure?"
                        message={`This action will delete ${mapping.keyword} with its mappings permanently!`}
                        handleAction={() => useKeywordMappingsStore.getState().deleteMapping(mapping.uid)}
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

export default KeywordMapping
