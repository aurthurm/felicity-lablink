import { useNavigate } from 'react-router-dom';
import {
    FileSpreadsheet,
    LogOut,
    Settings,
    MonitorDot,
    BarChart2,
  } from "lucide-react"
  
  import { Button } from "@/components/ui/button"
 
  import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
  } from "@/components/ui/tooltip"

  import { useAuthStore } from '@/store/auth';
import { useEffect } from 'react';

  
  export default function AsideBar() {
    const navigate = useNavigate();
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

    useEffect(() => {
        if(!isAuthenticated) navigate("/login")
    },[isAuthenticated])

    const handleLogout = () => {
        useAuthStore.getState().logout()
        navigate('/login');
    }

    return (
        <aside className="inset-y fixed  left-0 z-20 flex h-full flex-col border-r">
        <div className="border-b p-2">
            <Button variant="outline" size="icon" aria-label="Home" onClick={() => navigate("/")}>
                <BarChart2 className="size-5 fill-foreground" />
            </Button>
        </div>
        <nav className="grid gap-1 p-2">
            <Tooltip>
                <TooltipTrigger asChild>
                    <Button
                    variant="ghost"
                    size="icon"
                    className="rounded-lg"
                    aria-label="Orders"
                    onClick={() => navigate("/orders")}
                    >
                    <FileSpreadsheet className="size-5" />
                    </Button>
                </TooltipTrigger>
                <TooltipContent side="right" sideOffset={5}>
                    Orders
                </TooltipContent>
            </Tooltip>
            <Tooltip>
                <TooltipTrigger asChild>
                    <Button
                    variant="ghost"
                    size="icon"
                    className="rounded-lg bg-muted"
                    aria-label="Instruments"
                    onClick={() => navigate("/instruments")}
                    >
                    <MonitorDot className="size-5" />
                    </Button>
                </TooltipTrigger>
                <TooltipContent side="right" sideOffset={5}>
                    Instruments
                </TooltipContent>
            </Tooltip>
        </nav>
        <nav className="mt-auto grid gap-1 p-2">
            <Tooltip>
            <TooltipTrigger asChild>
                <Button
                variant="ghost"
                size="icon"
                className="mt-auto rounded-lg"
                aria-label="Settings"
                onClick={() => navigate("/settings")}
                >
                <Settings className="size-5" />
                </Button>
            </TooltipTrigger>
            <TooltipContent side="right" sideOffset={5}>
                Settings
            </TooltipContent>
            </Tooltip>
            <Tooltip>
            <TooltipTrigger asChild>
                <Button
                variant="ghost"
                size="icon"
                className="mt-auto rounded-lg"
                aria-label="Logout"
                onClick={() => handleLogout()}
                >
                <LogOut className="size-5" />
                </Button>
            </TooltipTrigger>
            <TooltipContent side="right" sideOffset={5} >
                Logout
            </TooltipContent>
            </Tooltip>
        </nav>
        </aside>
    )
  }
  