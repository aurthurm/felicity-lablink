import LayoutAdmin from "@/components/layouts/admin";
import {Link} from 'react-router-dom';

function SettingsLayout({ children }: any) {
  return (
    <LayoutAdmin>
      <div className="">
        <div className="ml-8 grid w-full max-w-7xl gap-2 mb-4">
          <h1 className="text-3xl font-semibold">Settings</h1>
          <p className=" text-slate-500 font-light text-sm">Manage your LabLik settings</p>
        </div>
        <hr />
        <div className="ml-8 pt-8 grid w-full max-w-7xl items-start gap-6 md:grid-cols-[180px_1fr] lg:grid-cols-[250px_1fr]">
          <nav
            className="grid gap-4 text-sm text-muted-foreground" x-chunk="dashboard-04-chunk-0"
          >
            <Link to="/settings" className="font-semibold text-primary">
              General
            </Link>
            <Link to="/settings/lims">Lims</Link>
            <Link to="/settings/mappings">Mappings</Link>
            <Link to="/settings/translations">Translations</Link>
            <Link to="/settings/exclusions">Exclusions</Link>
          </nav>
          <div className="grid gap-6">
            {children}
          </div>
        </div>
      </div>
    </LayoutAdmin>
  )
}

export default SettingsLayout