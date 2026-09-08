"use client"

import { Button } from "@/components/ui/button"
import axios from "axios"
import { useRouter } from "next/navigation"
import { useState } from "react"

type ApiError = {
    error: {
        code: string
        message: string
    }
}

const Dashboard = () => {
    const router = useRouter()
    
    const handleLogout = async () => {
        try {
            localStorage.removeItem("access_token")
            router.push("/login")
        } catch (error) {
            console.error("Logout error:", error)
        }
    }

    return (
        <div className="">
        <div className="min-h-screen w-full flex items-center justify-center bg-white p-8 text-6xl"
        >Welcome to my dashboard
        </div>
        <Button
        className="mb-32 cursor-pointer bg-blue-600"
         onClick={handleLogout}>Logout</Button>
        </div>
    )
}

export default Dashboard