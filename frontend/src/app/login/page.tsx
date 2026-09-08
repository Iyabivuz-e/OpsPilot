"use client"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import axios from "axios"
import { useRouter } from "next/navigation"

type LoginProps = {
    email: string
}

const Login = ({email}: LoginProps) => {
    const [emailValue, setEmailValue] = useState(email || "")
    const [isLoading, setIsLoading] = useState(false)

    const router = useRouter()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsLoading(true)

        try {
            const response = await axios.post("http://localhost:8000/api/v1/login", {
                email: emailValue
            })
            console.log("Response", response.data)

            if (response.status == 200){
                router.push('/dashboard')
            }
        } catch (error: any) {
            console.log(error.response?.status)
            console.log(error.response?.data)

            console.log("something happened")
        }
        // once all good
        setIsLoading(false)
    }

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-white p-8">
            <div className="w-full max-w-md flex flex-col items-center">
                <div className="flex items-center justify-center mb-8">
                <h1 className="text-6xl font-semibold text-slate-900 text-center">
                    Welcome to OpsPilot-
                </h1>
                </div>
        
                <Card className="w-full p-6 mt-4 border border-blue-100 shadow-sm bg-white">
                <form onSubmit={handleSubmit} className="w-full space-y-4">
                    <div className="space-y-2">
                    <Label htmlFor="email" className="text-slate-700">
                        Email
                    </Label>
                    <Input
                        className="p-4 border-blue-200 focus-visible:ring-blue-400"
                        id="email"
                        type="email"
                        placeholder="email..."
                        value={emailValue}
                        onChange={(e) => setEmailValue(e.target.value)}
                    />
                    </div>
        
                    <Button
                    type="submit"
                    disabled={isLoading}
                    className="w-full cursor-pointer bg-blue-600 hover:bg-blue-700 text-white"
                    >
                    {isLoading ? "Logging in..." : "Log in"}
                    </Button>
                </form>
                </Card>
            </div>
        </div>

    )
}
export default Login