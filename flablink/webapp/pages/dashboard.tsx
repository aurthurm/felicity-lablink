import InstrumentCard from "@/components/dashboard/instrument-card";
import LayoutAdmin from "@/components/layouts/admin";

import { useInstrumentsStore } from "@/store/instruments";

function DashBoardPage() {
  const instruments = useInstrumentsStore((state) => state.instruments)
  return (
    <LayoutAdmin>
      <div className="grid grid-cols-12 w-full">
        <div className="col-span-9"></div>
        <div className="col-span-3 flex flex-col gap-2">
          {instruments.map((instrument) => (<InstrumentCard instrument={instrument} />))}
        </div>
      </div>
    </LayoutAdmin>
  )
}

export default DashBoardPage
