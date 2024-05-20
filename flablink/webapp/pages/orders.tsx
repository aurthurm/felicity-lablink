import { Grid, _ } from 'gridjs-react';
import { RowSelection } from "gridjs/plugins/selection";

import "gridjs/dist/theme/mermaid.css";

import {
  DotsHorizontalIcon,
} from "@radix-ui/react-icons"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"

import LayoutAdmin from "@/components/layouts/admin";
import { Order } from "@/store/orders"
import {  useState } from 'react';
import { useUrl } from '../utils';
import { Checkbox } from "@/components/ui/checkbox"


function OrdersPage() {
  const [searchServer, setSearchServer] = useState(true);
 const syncState = (sync: number) => {
  switch (sync) {
    case 0:
      return "pending"
    case 1:
      return "synced"
    default:
      return "skipped"
  } 
 }
  return (
    <LayoutAdmin>

      <div className="flex items-center">
        <div className="flex items-center space-x-2">
          <Checkbox id="serverSearch" 
            checked={searchServer} 
            onCheckedChange={() => setSearchServer((p) => !p)} 
          />
          <label
            htmlFor="serverSearch"
            className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            Server Search
          </label>
        </div>
      </div>

      <Grid
        columns={[
          // {
          //   id: 'myCheckbox',
          //   name: 'Select',
          //   plugin: {
          //     component: RowSelection,
          //   }
          // },
          "Test Id",
          "Keyword",
          "Result",
          "Result Date",
          "Unit",
          "Synced",
          "Sync Date",
          "Instrument",
          'Actions'
        ]}
        search={searchServer ? {
          server: {
            url: (prev, keyword) => `${prev}?filter=${keyword}`
          }
        } : true }
        pagination={{
          limit: 10,
        }}
        server={{
          url: useUrl("/orders"),
          then: data => data.map((order: Order) => [
            order.test_id, order.keyword, order.result,
            order.result_date, order.unit, syncState(+order.synced),
            order.sync_date, order.instrument, 
            _(<DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="h-8 w-8 p-0">
                  <span className="sr-only">Open menu</span>
                  <DotsHorizontalIcon className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel>Actions</DropdownMenuLabel>
                <DropdownMenuItem
                  onClick={() => navigator.clipboard.writeText(order.raw_message ?? "")}
                >
                  Copy Raw Message
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                {/* <DropdownMenuItem>View customer</DropdownMenuItem> */}
              </DropdownMenuContent>
            </DropdownMenu>)
          ])
        }
        } 
      />
    </LayoutAdmin>
  )
}

export default OrdersPage;
