import { UserResource } from "./user.resource";
import { AuthResource } from "./auth.resource";
import { ProjectResource } from "./project.resource";
import { ExperienceResource } from "./experience.resource";
import { FeedbackResource } from "./feedback.resource";
import { PostResource } from "./post.resource";

export default {
    user: new UserResource(),
    auth: new AuthResource(),
    project: new ProjectResource(),
    post: new PostResource(),
    experience: new ExperienceResource(),
    feedback: new FeedbackResource(),
};