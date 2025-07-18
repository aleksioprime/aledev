import { UserResource } from "./user.resource";
import { AuthResource } from "./auth.resource";
import { ProjectResource } from "./project.resource";
import { ExperienceResource } from "./experience.resource";
import { FeedbackResource } from "./feedback.resource";

export default {
    user: new UserResource(),
    auth: new AuthResource(),
    project: new ProjectResource(),
    experience: new ExperienceResource(),
    feedback: new FeedbackResource(),
};