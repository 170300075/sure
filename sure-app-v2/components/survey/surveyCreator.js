"use client"

import { Button } from "@components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@components/ui/card"
import { Input } from "@components/ui/input"
import { Label } from "@components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@components/ui/select"
import { Textarea } from "@components/ui/textarea"

export function SurveyCreator() {
  return (
    <Card className="w-[500px]">
      <CardHeader>
        <CardTitle>Create a new survey</CardTitle>
        <CardDescription>
          Please, provide the information about your survey
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-6">
        <div className="grid grid-cols-2 gap-4">
          <div className="grid gap-2">
            <Label htmlFor="area">Company</Label>
            <Select>
              <SelectTrigger id="area" className="w-full">
                <SelectValue placeholder="Select a company" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="team">Syno Cancun</SelectItem>
                <SelectItem value="billing">Syno Vilnius</SelectItem>
                <SelectItem value="account">Wahsel</SelectItem>
                <SelectItem value="deployments">McKinsey</SelectItem>
                <SelectItem value="support">Interpret</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="grid gap-2">
            <Label htmlFor="security-level">Survey visibility</Label>
            <Select>
              <SelectTrigger
                id="security-level"
                className="line-clamp-1 w-full truncate"
              >
                <SelectValue placeholder="Choose a visibility" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 inline-block mr-3">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    Public
                </SelectItem>
                <SelectItem value="2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 inline-block mr-3">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                    Private
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
        <div className="grid gap-2">
            <Label htmlFor="project">Link to project <small className="text-slate-500">(Optional)</small></Label>
            <Select>
                <SelectTrigger id="project">
                    <SelectValue placeholder="Select a project name" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="none">None of these</SelectItem>
                    <SelectItem value="team">P4087 XXL Pilot June 2023</SelectItem>
                    <SelectItem value="billing">P4078 Ad Test Portugal</SelectItem>
                    <SelectItem value="account">P4102 Alcohol consumption</SelectItem>
                    <SelectItem value="deployments">P3843 Nelly's customers and panelists</SelectItem>
                </SelectContent>
            </Select>
        </div>

        <div className="grid gap-2">
          <Label htmlFor="subject">Survey name</Label>
          <Input id="subject" placeholder="Use a descriptive name" />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="description">Description</Label>
          <Textarea
            id="description"
            placeholder="Please include all information relevant to your survey"
          />
        </div>
      </CardContent>
      <CardFooter className="justify-between space-x-2">
        <Button variant="ghost">Cancel</Button>
        <Button className="bg-blue-500 shadow-lg shadow-blue-200">Create</Button>
      </CardFooter>
    </Card>
  )
}